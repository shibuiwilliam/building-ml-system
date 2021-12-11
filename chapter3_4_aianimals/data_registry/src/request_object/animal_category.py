from typing import Optional

from pydantic import BaseModel, Extra


class AnimalCategoryRequest(BaseModel):
    id: Optional[int]
    name_en: Optional[str]
    name_ja: Optional[str]
    is_deleted: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalCategoryCreateRequest(BaseModel):
    id: int
    name_en: str
    name_ja: str

    class Config:
        extra = Extra.forbid
