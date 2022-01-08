from datetime import datetime
from typing import Optional

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


class AnimalDocument(BaseModel):
    name: str
    description: str
    photo_url: str
    animal_category_name_en: str
    animal_category_name_ja: str
    animal_subcategory_name_en: str
    animal_subcategory_name_ja: str
    user_handle_name: str
    created_at: datetime

    class Config:
        extra = Extra.forbid


ANIMAL_MAPPING_NAME = "animal"

ANIMAL_MAPPING = {
    "settings": {
        "analysis": {
            "analyzer": {
                "kuromoji_analyzer": {
                    "type": "custom",
                    "char_filter": [
                        "icu_normalizer",
                    ],
                    "tokenizer": "kuromoji_tokenizer",
                    "filter": [
                        "kuromoji_baseform",
                        "kuromoji_part_of_speech",
                        "ja_stop",
                        "kuromoji_number",
                        "kuromoji_stemmer",
                    ],
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "name": {
                "type": "text",
                "analyzer": "kuromoji_analyzer",
            },
            "description": {
                "type": "text",
                "analyzer": "kuromoji_analyzer",
            },
            "animal_category_name_en": {
                "type": "text",
            },
            "animal_category_name_ja": {
                "type": "text",
                "analyzer": "kuromoji_analyzer",
            },
            "animal_subcategory_name_en": {
                "type": "text",
            },
            "animal_subcategory_name_ja": {
                "type": "text",
                "analyzer": "kuromoji_analyzer",
            },
            "user_handle_name": {
                "type": "text",
            },
            "created_at": {
                "type": "date",
            },
        }
    },
}
