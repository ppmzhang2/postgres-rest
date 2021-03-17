from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.models.dao import Dao
from app.schema.common_response import NumResponse

_dao = Dao()
router = APIRouter()


@router.get('/sales', response_model=NumResponse)
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
        sales = _dao.total_sales_amount(dt=dt_str)
        return NumResponse(result=sales)
