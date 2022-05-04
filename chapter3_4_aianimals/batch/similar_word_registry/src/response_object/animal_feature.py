from typing import List

from pydantic import BaseModel, Extra


class AnimalFeatureInitializeResponse(BaseModel):
    animal_category_vectorizer_file: str
    animal_subcategory_vectorizer_file: str
    description_vectorizer_file: str
    name_vectorizer_file: str
    animal_ids: List[str]

    class Config:
        extra = Extra.forbid
