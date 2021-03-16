from app import cfg
from app.middleware import app
from app.routers import config, summary

app.include_router(
    config.router,
    prefix=f'{cfg.REST_URL_PREFIX}/config',
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
