from typing import Optional

from pydantic import BaseModel, Extra


class LikeRequest(BaseModel):
    id: Optional[str]
    content_id: Optional[str]
    user_id: Optional[str]

    class Config:
        extra = Extra.forbid


class LikeCreateRequest(BaseModel):
    content_id: str
    user_id: str

    class Config:
        extra = Extra.forbid


class LikeDeleteRequest(BaseModel):
    id: str

    class Config:
        extra = Extra.forbid
