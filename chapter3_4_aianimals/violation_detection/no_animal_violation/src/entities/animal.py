from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class AnimalQuery(BaseModel):
    id: Optional[str]

    class Config:
        extra = Extra.forbid


class AnimalModel(BaseModel):
    id: str
    animal_category_id: int
    animal_subcategory_id: int
    name: str
    description: str
    photo_url: str
    deactivated: bool = False
    user_id: str
    created_at: datetime
    updated_at: datetime
