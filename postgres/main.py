from datetime import datetime

from fastapi import FastAPI, HTTPException

from postgres import cfg
from postgres.models.dao import Dao

app = FastAPI()
_dao = Dao()


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
