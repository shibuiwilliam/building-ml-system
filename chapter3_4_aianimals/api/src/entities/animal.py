from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra

ANIMAL_INDEX = "animal"


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


class AnimalSearchSortKey(Enum):
    SCORE = "score"
    LIKE = "like"
    CREATED_AT = "created_at"
    RANDOM = "random"
    LEARN_TO_RANK = "learn_to_rank"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in AnimalSearchSortKey.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in AnimalSearchSortKey.__members__.values()]

    @staticmethod
    def value_to_key(value: Optional[str] = None) -> Optional[Enum]:
        if value is None:
            return None
        for v in [v for v in AnimalSearchSortKey.__members__.values()]:
            if value == v.value:
                return v
        return None


class AnimalSearchQuery(BaseModel):
    user_id: Optional[str]
    animal_category_name_en: Optional[str]
    animal_category_name_ja: Optional[str]
    animal_subcategory_name_en: Optional[str]
    animal_subcategory_name_ja: Optional[str]
    phrases: List[str]
    sort_by: AnimalSearchSortKey = AnimalSearchSortKey.SCORE

    class Config:
        extra = Extra.forbid


class AnimalSearchResult(BaseModel):
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


class AnimalSearchResults(BaseModel):
    hits: int
    max_score: Optional[float]
    results: List[AnimalSearchResult]
    offset: int

    class Config:
        extra = Extra.forbid
