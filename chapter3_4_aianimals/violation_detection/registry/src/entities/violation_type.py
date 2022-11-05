from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class ViolationTypeQuery(BaseModel):
    id: Optional[str]
    name: Optional[str]

    class Config:
        extra = Extra.forbid


class ViolationTypeCreate(BaseModel):
    id: str
    name: str

    class Config:
        extra = Extra.forbid


class ViolationTypeDelete(BaseModel):
    id: str

    class Config:
        extra = Extra.forbid


class ViolationTypeModel(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
