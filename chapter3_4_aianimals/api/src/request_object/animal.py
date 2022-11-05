import json
from typing import List, Optional

from pydantic import BaseModel, Extra


class AnimalRequest(BaseModel):
    id: Optional[str]
    name: Optional[str]
    animal_category_id: Optional[int]
    animal_subcategory_id: Optional[int]
    user_id: Optional[str]
    deactivated: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalCreateRequest(BaseModel):
    animal_category_id: int
    animal_subcategory_id: int
    user_id: str
    name: str
    description: str

    class Config:
        extra = Extra.forbid

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class AnimalSearchRequest(BaseModel):
    user_id: Optional[str]
    animal_category_name_en: Optional[str]
    animal_category_name_ja: Optional[str]
    animal_subcategory_name_en: Optional[str]
    animal_subcategory_name_ja: Optional[str]
    phrases: List[str]
    sort_by: Optional[str] = "score"

    class Config:
        extra = Extra.forbid


class SimilarAnimalSearchRequest(BaseModel):
    id: str

    class Config:
        extra = Extra.forbid
