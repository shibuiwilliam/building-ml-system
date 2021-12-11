from datetime import datetime

from pydantic import BaseModel, Extra


class AnimalCategoryResponse(BaseModel):
    id: int
    name_en: str
    name_ja: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
