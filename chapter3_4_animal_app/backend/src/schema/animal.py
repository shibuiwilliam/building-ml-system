from datetime import datetime
from typing import Optional

from src.schema.abstract_schema import AbstractCreate, AbstractModel, AbstractQuery


class AnimalQuery(AbstractQuery):
    id: Optional[str]
    name: Optional[str]
    animal_category_id: Optional[str]
    animal_subcategory_id: Optional[str]
    user_id: Optional[str]
    deactivated: Optional[bool] = False


class AnimalCreate(AbstractCreate):
    id: str
    animal_category_id: str
    animal_subcategory_id: str
    user_id: str
    name: str
    description: str
    photo_url: str


class AnimalModel(AbstractModel):
    id: str
    animal_category_id: str
    animal_category_name: str
    animal_subcategory_id: str
    animal_subcategory_name: str
    user_id: str
    user_handle_name: str
    name: str
    description: str
    photo_url: str
    deactivated: bool = False
    created_at: datetime
    updated_at: datetime
