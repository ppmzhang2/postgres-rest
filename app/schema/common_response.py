import pydantic


class PkidResponse(pydantic.BaseModel):
    pkid: int


class NumResponse(pydantic.BaseModel):
    result: int


class MsgResponse(pydantic.BaseModel):
    message: str
