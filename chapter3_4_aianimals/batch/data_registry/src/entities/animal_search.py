from datetime import datetime

from pydantic import BaseModel, Extra


class AnimalDocument(BaseModel):
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
            "like": {
                "type": "integer",
            },
            "created_at": {
                "type": "date",
            },
        }
    },
}
