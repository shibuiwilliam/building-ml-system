from datetime import datetime

from pydantic import BaseModel, Extra


class AnimalResponseBase(BaseModel):
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


class AnimalResponse(AnimalResponseBase):
    pass

    class Config:
        extra = Extra.forbid
