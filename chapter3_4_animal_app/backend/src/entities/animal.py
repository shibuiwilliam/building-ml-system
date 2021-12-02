from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class AnimalQuery(BaseModel):
    id: Optional[str]
    name: Optional[str]
    animal_category_id: Optional[str]
    animal_subcategory_id: Optional[str]
    user_id: Optional[str]
    deactivated: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalCreate(BaseModel):
    id: str
    animal_category_id: str
    animal_subcategory_id: str
    user_id: str
    name: str
    description: str
    photo_url: str

    class Config:
        extra = Extra.forbid


class AnimalModelBase(BaseModel):
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


class AnimalModel(AnimalModelBase):
    pass

    class Config:
        extra = Extra.forbid


class AnimalModelWithLike(AnimalModelBase):
    like: int

    class Config:
        extra = Extra.forbid
