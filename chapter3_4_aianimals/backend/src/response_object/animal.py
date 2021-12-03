from datetime import datetime

from pydantic import BaseModel, Extra


class AnimalResponseBase(BaseModel):
    id: str
    animal_category_id: int
    animal_category_name: str
    animal_subcategory_id: int
    animal_subcategory_name: str
    user_id: str
    user_handle_name: str
    name: str
    description: str
    photo_url: str
    deactivated: bool = False
    created_at: datetime
    updated_at: datetime


class AnimalResponse(AnimalResponseBase):
    pass

    class Config:
        extra = Extra.forbid


class AnimalResponseWithLike(AnimalResponseBase):
    like: int

    class Config:
        extra = Extra.forbid