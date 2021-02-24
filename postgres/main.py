from datetime import datetime

from fastapi import HTTPException

from postgres import cfg
from postgres.models.dao import Dao

from .middleware import app

_dao = Dao()


@app.post(f'{cfg.REST_URL_PREFIX}/init/')
async def init_db():
    try:
        _dao.drop_all()
        _dao.create_all()
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail='cannot execute now',
        ) from err
    else:
        return {'message': 'success'}


@app.get(f'{cfg.REST_URL_PREFIX}/sales')
async def total_sales(date: str):
    fmt = '%Y-%m-%d'
    try:
        dt = datetime.strptime(date, fmt)
        dt_str = dt.strftime(fmt)
    except (ValueError, TypeError) as err:
        raise HTTPException(
            status_code=400,
            detail='parameter "date" accept only "yyyy-mm-dd" format',
        ) from err
    else:
        sales = _dao.total_sales(dt=dt_str)
        return {'sales': sales}
