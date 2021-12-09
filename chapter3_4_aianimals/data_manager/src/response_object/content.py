from datetime import datetime

from pydantic import BaseModel, Extra


class ContentResponseBase(BaseModel):
    id: str
    user_id: str
    user_handle_name: str
    name: str
    description: str
    photo_url: str
    deactivated: bool = False
    created_at: datetime
    updated_at: datetime


class ContentResponse(ContentResponseBase):
    pass

    class Config:
        extra = Extra.forbid


class ContentResponseWithLike(ContentResponseBase):
    like: int

    class Config:
        extra = Extra.forbid
