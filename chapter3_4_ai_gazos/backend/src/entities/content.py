from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class ContentQuery(BaseModel):
    id: Optional[str]
    name: Optional[str]
    user_id: Optional[str]
    deactivated: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class ContentCreate(BaseModel):
    id: str
    user_id: str
    name: str
    description: str
    photo_url: str
    created_at: Optional[datetime]

    class Config:
        extra = Extra.forbid


class ContentModelBase(BaseModel):
    id: str
    user_id: str
    user_handle_name: str
    name: str
    description: str
    photo_url: str
    deactivated: bool = False
    created_at: datetime
    updated_at: datetime


class ContentModel(ContentModelBase):
    pass

    class Config:
        extra = Extra.forbid


class ContentModelWithLike(ContentModelBase):
    like: int

    class Config:
        extra = Extra.forbid
