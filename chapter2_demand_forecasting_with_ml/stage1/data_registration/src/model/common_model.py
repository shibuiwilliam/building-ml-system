from pydantic import BaseModel, Extra


class Count(BaseModel):
    count: int = 0

    class Config:
        extra = Extra.forbid


class Exists(BaseModel):
    exists: bool

    class Config:
        extra = Extra.forbid
