import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app import cfg
from app.middleware import app
from app.routers import category, config, summary
from app.schema.api_exception import ApiException

logging.config.dictConfig(cfg.LOGGING)
logger = logging.getLogger()

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
    content = {
        'category': exception.category,
        'message': exception.message,
    }
    response = JSONResponse(status_code=exception.status_code, content=content)
    logger.error({'error': repr(exception)})
    return response
