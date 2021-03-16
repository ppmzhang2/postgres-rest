from functools import wraps

from fastapi import APIRouter, HTTPException

from app.models.dao import Dao
from app.schema.common_response import MsgResponse, NumResponse

_dao = Dao()
router = APIRouter()


def try_catch(fn):
    @wraps(fn)
    def helper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as err:
            raise HTTPException(
                status_code=500,
                detail='cannot execute now',
            ) from err

    return helper


@try_catch
@router.post('/init', response_model=MsgResponse)
async def init_db():
    _dao.drop_all()
    _dao.create_all()
    return MsgResponse(message='success')


@try_catch
@router.post('/load', response_model=MsgResponse)
async def load_txt():
    _dao.load_sample()
    return MsgResponse(message='success')


@router.get('/count/{table}', response_model=NumResponse)
async def record_count(table: str):
    dc_func = {
        'user': _dao.count_users,
        'listing': _dao.count_listings,
        'category': _dao.count_categories
    }
    try:
        func = dc_func[table]
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f'can only count {dc_func.keys()}',
        ) from e
    return NumResponse(result=func())
