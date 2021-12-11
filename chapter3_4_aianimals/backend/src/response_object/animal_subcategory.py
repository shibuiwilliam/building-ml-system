from datetime import datetime

from pydantic import BaseModel, Extra


class AnimalSubcategoryResponse(BaseModel):
    id: int
    animal_category_id: int
    animal_category_name_en: str
    animal_category_name_ja: str
    name_en: str
    name_ja: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
