from typing import Optional

from pydantic import BaseModel, Extra


class AnimalSubcategoryRequest(BaseModel):
    id: Optional[str]
    animal_category_name: Optional[str]
    name: Optional[str]
    is_deleted: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalSubcategoryCreateRequest(BaseModel):
    id: str
    animal_category_id: str
    name: str

    class Config:
        extra = Extra.forbid
