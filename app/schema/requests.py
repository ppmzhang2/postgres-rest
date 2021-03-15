import pydantic


class ReqAddCategory(pydantic.BaseModel):
    group: str
    name: str
    description: str


class RespCategory(ReqAddCategory):
    pkid: int
