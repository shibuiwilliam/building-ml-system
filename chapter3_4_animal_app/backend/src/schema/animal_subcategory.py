from datetime import datetime
from typing import Optional

from src.schema.abstract_schema import AbstractCreate, AbstractModel, AbstractQuery


class AnimalSubcategoryQuery(AbstractQuery):
    id: Optional[str]
    animal_category_id: Optional[str]
    name: Optional[str]
    is_deleted: Optional[bool] = False


class AnimalSubcategoryCreate(AbstractCreate):
    id: str
    animal_category_id: str
    name: str


class AnimalSubcategoryModel(AbstractModel):
    id: str
    animal_category_id: str
    animal_category_name: str
    name: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
