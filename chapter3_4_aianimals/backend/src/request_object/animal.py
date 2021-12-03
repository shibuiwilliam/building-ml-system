from typing import Optional

from pydantic import BaseModel, Extra


class AnimalRequest(BaseModel):
    id: Optional[str]
    name: Optional[str]
    animal_category_id: Optional[int]
    animal_subcategory_id: Optional[int]
    user_id: Optional[str]
    deactivated: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalCreateRequest(BaseModel):
    animal_category_id: int
    animal_subcategory_id: int
    user_id: str
    name: str
    description: str

    class Config:
        extra = Extra.forbid
