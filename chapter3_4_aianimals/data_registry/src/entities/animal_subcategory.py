from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class AnimalSubcategoryQuery(BaseModel):
    id: Optional[int]
    animal_category_id: Optional[int]
    name: Optional[str]
    is_deleted: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalSubcategoryCreate(BaseModel):
    id: int
    animal_category_id: int
    name: str

    class Config:
        extra = Extra.forbid


class AnimalSubcategoryModel(BaseModel):
    id: int
    animal_category_id: int
    name: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
