from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra


class AnimalResponseBase(BaseModel):
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
    like: int
    deactivated: bool = False
    created_at: datetime
    updated_at: datetime


class AnimalResponse(AnimalResponseBase):
    pass

    class Config:
        extra = Extra.forbid


class AnimalSearchResponse(BaseModel):
    score: Optional[float]
    id: str
    name: str
    description: str
    photo_url: str
    animal_category_name_en: str
    animal_category_name_ja: str
    animal_subcategory_name_en: str
    animal_subcategory_name_ja: str
    user_handle_name: str
    like: int
    created_at: datetime

    class Config:
        extra = Extra.forbid


class AnimalSearchResponses(BaseModel):
    hits: int
    max_score: Optional[float]
    results: List[AnimalSearchResponse]
    offset: int
    search_id: str
    sort_by: str
    model_name: Optional[str] = None

    class Config:
        extra = Extra.forbid


class SimilarAnimalSearchResponse(BaseModel):
    id: str
    name: str
    description: str
    photo_url: str
    animal_category_name_en: str
    animal_category_name_ja: str
    animal_subcategory_name_en: str
    animal_subcategory_name_ja: str
    user_handle_name: str
    like: int
    created_at: datetime

    class Config:
        extra = Extra.forbid


class SimilarAnimalSearchResponses(BaseModel):
    results: List[SimilarAnimalSearchResponse]
    search_id: str
    sort_by: str
    model_name: Optional[str] = None

    class Config:
        extra = Extra.forbid
