from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class AnimalSubcategoryQuery(BaseModel):
    id: Optional[str]
    animal_category_id: Optional[str]
    name: Optional[str]
    is_deleted: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalSubcategoryCreate(BaseModel):
    id: str
    animal_category_id: str
    name: str

    class Config:
        extra = Extra.forbid


class AnimalSubcategoryModel(BaseModel):
    id: str
    animal_category_id: str
    animal_category_name: str
    name: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
