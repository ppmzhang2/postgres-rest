from typing import List

from fastapi import APIRouter

from app.models.dao import Dao
from app.schema.category import CategoryResponse, NewCategoryRequest
from app.schema.common_response import PkidResponse

_dao = Dao()
router = APIRouter()


@router.get('', response_model=List[CategoryResponse])
async def all_cate(limit: int, offset: int):
    res = _dao.all_category(limit, offset)
    return res


@router.post('', response_model=PkidResponse)
async def new_cate(req: NewCategoryRequest):
    pkid = _dao.add_category(req.catgroup, req.catname, req.catdesc)
    return PkidResponse(pkid=pkid)


@router.get('/{pkid}', response_model=CategoryResponse)
async def lookup_cate(pkid: int):
    cate = _dao.lookup_category_id(pkid)
    return cate
