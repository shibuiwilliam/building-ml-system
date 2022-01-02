from typing import List

from pydantic import BaseModel, Extra
from src.response_object.animal_category import AnimalCategoryResponse
from src.response_object.animal_subcategory import AnimalSubcategoryResponse


class MetadataResponse(BaseModel):
    animal_category: List[AnimalCategoryResponse]
    animal_subcategory: List[AnimalSubcategoryResponse]

    class Config:
        extra = Extra.forbid
