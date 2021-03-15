from datetime import datetime
from functools import wraps

from fastapi import APIRouter, HTTPException

from app.models.dao import Dao
from app.schema.requests import ReqAddCategory

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
@router.post('/init/')
async def init_db():
    _dao.drop_all()
    _dao.create_all()
    return {'message': 'success'}


@try_catch
@router.post('/load/')
async def load_txt():
    _dao.load_sample()
    return {'message': 'success'}


@router.post('/count/{table}')
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
    return {'detail': func()}


@router.post('/new/cate/')
async def new_cate(req: ReqAddCategory):
    pkid = _dao.add_category(req.group, req.name, req.description)
    return {'detail': pkid}


@router.get('/sales')
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
        return {'sales': sales}