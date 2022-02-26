from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra


class AnimalQuery(BaseModel):
    id: Optional[str]
    ids: Optional[List[str]]
    name: Optional[str]
    animal_category_id: Optional[int]
    animal_subcategory_id: Optional[int]
    user_id: Optional[str]
    deactivated: Optional[bool]

    class Config:
        extra = Extra.forbid


class AnimalCreate(BaseModel):
    id: str
    animal_category_id: int
    animal_subcategory_id: int
    user_id: str
    name: str
    description: str
    photo_url: str
    deactivated: bool = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        extra = Extra.forbid


class AnimalUpdate(BaseModel):
    id: str
    name: Optional[str]
    animal_category_id: Optional[int]
    animal_subcategory_id: Optional[int]
    user_id: Optional[str]
    description: Optional[str]
    photo_url: Optional[str]
    deactivated: Optional[bool]

    class Config:
        extra = Extra.forbid


class AnimalModel(BaseModel):
    id: str
    animal_category_id: int
    animal_category_name_en: str
    animal_category_name_ja: str
    animal_subcategory_id: int
    animal_subcategory_name_en: str
    animal_subcategory_name_ja: str
    name: str
    description: str
    photo_url: str
    deactivated: bool = False
    user_id: str
    user_handle_name: str
    created_at: datetime
    updated_at: datetime
