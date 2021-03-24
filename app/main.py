import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import cfg
from app.middleware import app
from app.routers import category, config, summary
from app.schema.api_exception import ApiException, ErrorCategory

logging.config.dictConfig(cfg.LOGGING)
logger = logging.getLogger(cfg.LOGGER)

app.include_router(
    config.router,
    prefix=f'{cfg.REST_URL_PREFIX}/config',
    responses={404: {
        'detail': 'not found'
    }},
)

app.include_router(
    category.router,
    prefix=f'{cfg.REST_URL_PREFIX}/category',
    responses={404: {
        'detail': 'not found'
    }},
)

app.include_router(
    summary.router,
    prefix=f'{cfg.REST_URL_PREFIX}/summary',
    responses={404: {
        'detail': 'not found'
    }},
)


@app.exception_handler(ApiException)
async def api_exception_handler(_: Request, exception: ApiException):
    error_category = exception.category
    content = {
        'category': error_category,
        'message': exception.message,
    }
    response = JSONResponse(status_code=exception.status_code, content=content)
    if error_category == ErrorCategory.NOT_FOUND.value:
        logger.info('%s: %s', error_category, exception.message)
    else:
        logger.error('%s: %s', error_category, exception.message)
    return response


@app.exception_handler(RequestValidationError)
async def request_exception_handler(
    _: Request,
    exception: RequestValidationError,
):
    error_category = ErrorCategory.REQUEST_INVALID.value
    content = {
        'category': error_category,
        'message': repr(exception),
    }
    response = JSONResponse(status_code=400, content=content)
    logger.info('%s: %s', error_category, exception)
    return response


@app.exception_handler(Exception)
async def unexpected_exception_handler(_: Request, exception: Exception):
    error_category = ErrorCategory.OTHER
    content = {
        'category': error_category,
        'message': 'please contact the admin for help',
    }
    response = JSONResponse(status_code=500, content=content)
    logger.error('%s: %s', error_category, exception)
    return response
