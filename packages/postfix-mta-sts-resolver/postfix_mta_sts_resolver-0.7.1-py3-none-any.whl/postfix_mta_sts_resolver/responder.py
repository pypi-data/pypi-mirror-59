import asyncio
import logging
import time
import collections
import sys
import os
import socket
from functools import partial

import pynetstring

from .resolver import STSResolver, STSFetchResult
from .constants import QUEUE_LIMIT, CHUNK
from .utils import create_custom_socket, create_cache, filter_domain, is_ipaddr
from .base_cache import CacheEntry


ZoneEntry = collections.namedtuple('ZoneEntry', ('strict', 'resolver'))


# pylint: disable=too-many-instance-attributes
class STSSocketmapResponder:
    def __init__(self, cfg, loop):
        self._logger = logging.getLogger("STS")
        self._loop = loop
        if cfg.get('path') is not None:
            self._unix = True
            self._path = cfg['path']
            self._sockmode = cfg.get('mode')
        else:
            self._unix = False
            self._host = cfg['host']
            self._port = cfg['port']
        self._reuse_port = cfg['reuse_port']
        self._shutdown_timeout = cfg['shutdown_timeout']
        self._grace = cfg['cache_grace']

        # Construct configurations and resolvers for every socketmap name
        self._default_zone = ZoneEntry(cfg["default_zone"]["strict_testing"],
                                       STSResolver(loop=loop,
                                                   timeout=cfg["default_zone"]["timeout"]))

        self._zones = dict((k, ZoneEntry(zone["strict_testing"],
                                         STSResolver(loop=loop,
                                                     timeout=zone["timeout"])))
                           for k, zone in cfg["zones"].items())

        # Construct cache
        self._cache = create_cache(cfg["cache"]["type"],
                                   cfg["cache"]["options"])
        self._children = set()
        self._server = None

    async def start(self):
        def _spawn(reader, writer):
            def done_cb(task, fut):
                self._children.discard(task)
            task = self._loop.create_task(self.handler(reader, writer))
            task.add_done_callback(partial(done_cb, task))
            self._children.add(task)
            self._logger.debug("len(self._children) = %d", len(self._children))

        await self._cache.setup()

        if self._unix:
            self._server = await asyncio.start_unix_server(_spawn, path=self._path)
            if self._sockmode is not None:
                os.chmod(self._path, self._sockmode)
        else:
            if self._reuse_port: # pragma: no cover
                if sys.platform in ('win32', 'cygwin'):
                    opts = {
                        'host': self._host,
                        'port': self._port,
                        'reuse_address': True,
                    }
                elif os.name == 'posix':
                    if sys.platform.startswith('freebsd'):
                        sockopts = [
                            (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
                            (socket.SOL_SOCKET, 0x10000, 1),  # SO_REUSEPORT_LB
                        ]
                        sock = await create_custom_socket(self._host, self._port,
                                                          options=sockopts)
                        opts = {
                            'sock': sock,
                        }
                    else:
                        opts = {
                            'host': self._host,
                            'port': self._port,
                            'reuse_address': True,
                            'reuse_port': True,
                        }
            self._server = await asyncio.start_server(_spawn, **opts)

    async def stop(self):
        self._server.close()
        await self._server.wait_closed()
        while True:
            self._logger.warning("Awaiting %d client handlers to finish...",
                                 len(self._children))
            remaining = asyncio.gather(*self._children, return_exceptions=True)
            self._children.clear()
            try:
                await asyncio.wait_for(remaining, self._shutdown_timeout)
            except asyncio.TimeoutError:
                self._logger.warning("Shutdown timeout expired. "
                                     "Remaining handlers terminated.")
                try:
                    await remaining
                except asyncio.CancelledError:
                    pass
            await asyncio.sleep(1)
            if not self._children:
                break
        await self._cache.teardown()

    async def sender(self, queue, writer):
        def cleanup_queue():
            while not queue.empty():
                task = queue.get_nowait()
                try:
                    task.cancel()
                except Exception:  # pragma: no cover
                    pass

        try:
            while True:
                fut = await queue.get()
                # Check for shutdown
                if fut is None:
                    return
                self._logger.debug("Got new future from queue")
                data = await fut
                self._logger.debug("Future await complete: data=%s", repr(data))
                writer.write(data)
                self._logger.debug("Wrote: %s", repr(data))
                await writer.drain()
        except asyncio.CancelledError:
            cleanup_queue()
        except Exception as exc: # pragma: no cover
            self._logger.exception("Exception in sender coro: %s", exc)
            cleanup_queue()
        finally:
            writer.close()

    # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    async def process_request(self, raw_req):
        # Update local cache
        async def cache_set(domain, entry):
            try:
                await self._cache.set(domain, entry)
            except asyncio.CancelledError:  # pragma: no cover pylint: disable=try-except-raise
                raise
            except Exception as exc: # pragma: no cover
                self._logger.exception("Cache set failed: %s", str(exc))

        have_policy = True

        # Parse request and canonicalize domain
        req_zone, _, req_domain = raw_req.decode('latin-1').partition(' ')
        domain = filter_domain(req_domain)

        # Skip lookups for parent domain policies
        # Skip lookups to non-domains
        if domain.startswith('.') or is_ipaddr(domain):
            return pynetstring.encode('NOTFOUND ')

        # Find appropriate zone config
        if req_zone in self._zones:
            zone_cfg = self._zones[req_zone]
        else:
            zone_cfg = self._default_zone

        # Lookup for cached policy
        try:
            cached = await self._cache.get(domain)
        except asyncio.CancelledError:  # pragma: no cover pylint: disable=try-except-raise
            raise
        except Exception as exc:  # pragma: no cover
            self._logger.exception("Cache get failed: %s", str(exc))
            cached = None

        ts = time.time()  # pylint: disable=invalid-name
        # Check if cached record exists and recent enough to omit
        # DNS lookup and cache update
        if cached is None or ts - cached.ts > self._grace:
            self._logger.debug("Lookup PERFORMED: domain = %s", domain)
            # Check if newer policy exists or
            # retrieve policy from scratch if there is no cached one
            latest_pol_id = None if cached is None else cached.pol_id
            status, policy = await zone_cfg.resolver.resolve(domain, latest_pol_id)

            if status is STSFetchResult.NOT_CHANGED:
                cached = CacheEntry(ts, cached.pol_id, cached.pol_body)
                await cache_set(domain, cached)
            elif status is STSFetchResult.VALID:
                pol_id, pol_body = policy
                cached = CacheEntry(ts, pol_id, pol_body)
                await cache_set(domain, cached)
            else:
                if cached is None:
                    have_policy = False
                else:
                    # Check if cached policy is expired
                    if cached.pol_body['max_age'] + cached.ts < ts:
                        have_policy = False
        else:
            self._logger.debug("Lookup skipped: domain = %s", domain)


        if have_policy:
            mode = cached.pol_body['mode']
            # pylint: disable=no-else-return
            if mode == 'none' or (mode == 'testing' and not zone_cfg.strict):
                return pynetstring.encode('NOTFOUND ')
            else:
                assert cached.pol_body['mx'], "Empty MX list for restrictive policy!"
                mxlist = [mx.lstrip('*') for mx in set(cached.pol_body['mx'])]
                resp = "OK secure match=" + ":".join(mxlist)
                return pynetstring.encode(resp)
        else:
            return pynetstring.encode('NOTFOUND ')

    async def handler(self, reader, writer):
        # Construct netstring parser
        decoder = pynetstring.Decoder()

        # Construct queue for responses ordering
        queue = asyncio.Queue(QUEUE_LIMIT, loop=self._loop)

        # Create coroutine which awaits for steady responses and sends them
        sender = asyncio.ensure_future(self.sender(queue, writer), loop=self._loop)

        class ParserInvokationError(Exception):
            pass

        class EndOfStream(Exception):
            pass

        async def finalize():
            try:
                await queue.put(None)
            except asyncio.CancelledError:  # pragma: no cover
                sender.cancel()
                raise
            await sender

        try:
            while True:
                #Extract and parse requests
                part = await reader.read(CHUNK)
                if not part:
                    raise EndOfStream()
                self._logger.debug("Read: %s", repr(part))
                try:
                    requests = decoder.feed(part)
                except:
                    raise ParserInvokationError("Bad netstring protocol.")

                # Enqueue tasks for received requests
                for req in requests:
                    self._logger.debug("Enq request: %s", repr(req))
                    fut = asyncio.ensure_future(self.process_request(req), loop=self._loop)
                    await queue.put(fut)
        except ParserInvokationError:
            self._logger.warning("Bad netstring message received")
            await finalize()
        except (EndOfStream, ConnectionError, TimeoutError):
            self._logger.debug("Client disconnected")
            await finalize()
        except OSError as exc:  # pragma: no cover
            if exc.errno == 107:
                self._logger.debug("Client disconnected")
                await finalize()
            else:
                self._logger.exception("Unhandled exception: %s", exc)
                await finalize()
        except asyncio.CancelledError:
            sender.cancel()
            raise
        except Exception as exc:  # pragma: no cover
            self._logger.exception("Unhandled exception: %s", exc)
            await finalize()
