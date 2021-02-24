import inspect
import logging.config
from functools import wraps

from aiohttp.abc import Request


class LogMaker(object):
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    @staticmethod
    def _func_extra(fn):
        return {
            'real_module': inspect.getmodule(fn).__name__,
            'real_funcName': fn.__name__,
            'real_lineno': inspect.getsourcelines(fn)[1],
        }

    def __call__(self, fn):
        @wraps(fn)
        def helper(*args, **kwargs):
            extra = self._func_extra(fn)
            self._logger.debug('[STARTED]', extra=extra)
            try:
                return fn(*args, **kwargs)
            except Exception as ex:
                self._logger.error(f'{ex}', extra=extra)
                raise ex
            finally:
                self._logger.debug('[ENDED]', extra=extra)

        return helper


class LogDbApi(LogMaker):
    """logging decorator for DbApi REST coroutines

    """
    def __call__(self, fn):
        @wraps(fn)
        async def helper(instance, request: Request, *args, **kwargs):
            extra = self._func_extra(fn)
            self._logger.debug(
                f'[STARTED] {request.remote} | {request.query_string}',
                extra=extra)
            try:
                return await fn(instance, request, *args, **kwargs)
            except Exception as ex:
                self._logger.error(f'{ex}', extra=extra)
                raise ex
            finally:
                self._logger.debug('[ENDED]', extra=extra)

        return helper
