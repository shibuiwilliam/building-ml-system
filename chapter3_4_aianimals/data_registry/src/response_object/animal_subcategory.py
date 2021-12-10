from datetime import datetime

from pydantic import BaseModel, Extra


class AnimalSubcategoryResponse(BaseModel):
    id: int
    animal_category_id: int
    name: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
