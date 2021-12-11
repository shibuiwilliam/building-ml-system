from typing import Optional

from pydantic import BaseModel, Extra


class AnimalSubcategoryRequest(BaseModel):
    id: Optional[int]
    animal_category_id: Optional[str]
    name_en: Optional[str]
    name_ja: Optional[str]
    is_deleted: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalSubcategoryCreateRequest(BaseModel):
    id: int
    animal_category_id: int
    name_en: str
    name_ja: str

    class Config:
        extra = Extra.forbid
