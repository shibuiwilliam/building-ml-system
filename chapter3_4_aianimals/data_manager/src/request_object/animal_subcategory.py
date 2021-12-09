from typing import Optional

from pydantic import BaseModel, Extra


class AnimalSubcategoryRequest(BaseModel):
    id: Optional[int]
    animal_category_id: Optional[str]
    name: Optional[str]
    is_deleted: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalSubcategoryCreateRequest(BaseModel):
    id: int
    animal_category_id: int
    name: str

    class Config:
        extra = Extra.forbid
