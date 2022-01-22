from datetime import datetime

from pydantic import BaseModel, Extra


class AnimalUpdate(BaseModel):
    id: str
    deactivated: bool

    class Config:
        extra = Extra.forbid


class AnimalModel(BaseModel):
    id: str
    animal_category_id: int
    animal_subcategory_id: int
    name: str
    description: str
    photo_url: str
    deactivated: bool
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
