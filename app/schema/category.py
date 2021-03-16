from typing import Optional

import pydantic


class NewCategoryRequest(pydantic.BaseModel):
    catgroup: Optional[str]
    catname: Optional[str]
    catdesc: Optional[str]


class CategoryResponse(NewCategoryRequest):
    catid: int

    class Config:
        orm_mode = True
