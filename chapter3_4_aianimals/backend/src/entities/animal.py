from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra


class AnimalQuery(BaseModel):
    id: Optional[str]
    name: Optional[str]
    animal_category_id: Optional[int]
    animal_subcategory_id: Optional[int]
    user_id: Optional[str]
    deactivated: Optional[bool] = False

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
    created_at: Optional[datetime]

    class Config:
        extra = Extra.forbid


class AnimalModelBase(BaseModel):
    id: str
    animal_category_id: int
    animal_category_name_en: str
    animal_category_name_ja: str
    animal_subcategory_id: int
    animal_subcategory_name_en: str
    animal_subcategory_name_ja: str
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


class AnimalSearchQuery(BaseModel):
    animal_category_name_en: Optional[str]
    animal_category_name_ja: Optional[str]
    animal_subcategory_name_en: Optional[str]
    animal_subcategory_name_ja: Optional[str]
    phrases: List[str]

    class Config:
        extra = Extra.forbid


class AnimalSearchResult(BaseModel):
    score: float
    id: str
    name: str
    description: str
    photo_url: str
    animal_category_name_en: str
    animal_category_name_ja: str
    animal_subcategory_name_en: str
    animal_subcategory_name_ja: str
    user_handle_name: str

    class Config:
        extra = Extra.forbid


class AnimalSearchResults(BaseModel):
    hits: int
    max_score: float
    results: List[AnimalSearchResult]

    class Config:
        extra = Extra.forbid
