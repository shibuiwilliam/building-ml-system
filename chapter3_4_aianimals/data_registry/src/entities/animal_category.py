from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class AnimalCategoryQuery(BaseModel):
    id: Optional[int]
    name_en: Optional[str]
    name_ja: Optional[str]
    is_deleted: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalCategoryCreate(BaseModel):
    id: int
    name_en: str
    name_ja: str

    class Config:
        extra = Extra.forbid


class AnimalCategoryModel(BaseModel):
    id: int
    name_en: str
    name_ja: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
