import pydantic


class NewCategoryRequest(pydantic.BaseModel):
    group: str
    name: str
    description: str


class CategoryResponse(NewCategoryRequest):
    pkid: int
