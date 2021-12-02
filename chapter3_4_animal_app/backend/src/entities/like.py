from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class LikeQuery(BaseModel):
    id: Optional[str]
    animal_id: Optional[str]
    user_id: Optional[str]
    animal_name: Optional[str]

    class Config:
        extra = Extra.forbid


class LikeCreate(BaseModel):
    id: str
    animal_id: str
    user_id: str

    class Config:
        extra = Extra.forbid


class LikeModel(BaseModel):
    id: str
    animal_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
