from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class AnimalCategoryQuery(BaseModel):
    id: Optional[int]
    name: Optional[str]
    is_deleted: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalCategoryCreate(BaseModel):
    id: int
    name: str

    class Config:
        extra = Extra.forbid


class AnimalCategoryModel(BaseModel):
    id: int
    name: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
