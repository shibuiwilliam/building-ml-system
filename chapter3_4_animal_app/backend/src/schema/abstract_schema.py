from pydantic import BaseModel


class AbstractQuery(BaseModel):
    pass


class AbstractCreate(BaseModel):
    pass


class AbstractModel(BaseModel):
    pass
