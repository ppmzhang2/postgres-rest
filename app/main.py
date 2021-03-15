from app import cfg
from app.middleware import app
from app.routers import summary

app.include_router(
    summary.router,
    prefix=f'{cfg.REST_URL_PREFIX}',
    responses={404: {
        'detail': 'not found'
    }},
)
