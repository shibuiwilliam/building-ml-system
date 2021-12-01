from datetime import datetime
from typing import Optional

from src.schema.abstract_schema import AbstractCreate, AbstractModel, AbstractQuery


class LikeQuery(AbstractQuery):
    id: Optional[str]
    animal_id: Optional[str]
    user_id: Optional[str]
    animal_name: Optional[str]


class LikeCreate(AbstractCreate):
    id: str
    animal_id: str
    user_id: str


class LikeModel(AbstractModel):
    id: str
    animal_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
