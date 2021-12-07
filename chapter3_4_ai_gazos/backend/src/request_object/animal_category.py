from typing import Optional

from pydantic import BaseModel, Extra


class AnimalCategoryRequest(BaseModel):
    id: Optional[int]
    name: Optional[str]
    is_deleted: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalCategoryCreateRequest(BaseModel):
    name: str

    class Config:
        extra = Extra.forbid
