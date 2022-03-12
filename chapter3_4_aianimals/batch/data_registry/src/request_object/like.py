from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Extra


class LikeRequest(BaseModel):
    id: Optional[str]
    animal_id: Optional[str]
    user_id: Optional[str]

    class Config:
        extra = Extra.forbid


class LikeCreateRequest(BaseModel):
    id: Optional[str]
    animal_id: str
    user_id: str
    created_at: Optional[datetime]

    class Config:
        extra = Extra.forbid


class LikeDeleteRequest(BaseModel):
    id: str

    class Config:
        extra = Extra.forbid
