from datetime import datetime

from pydantic import BaseModel, Extra


class AnimalCategoryResponse(BaseModel):
    id: int
    name: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
