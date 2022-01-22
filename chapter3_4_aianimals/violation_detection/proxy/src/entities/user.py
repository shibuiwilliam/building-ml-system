from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class UserQuery(BaseModel):
    id: Optional[str]
    handle_name: Optional[str]
    email_address: Optional[str]
    age: Optional[int]
    gender: Optional[int]
    deactivated: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class UserCreate(BaseModel):
    id: str
    handle_name: str
    email_address: str
    password: str
    age: int
    gender: int
    created_at: Optional[datetime]

    class Config:
        extra = Extra.forbid


class UserModel(BaseModel):
    id: str
    handle_name: str
    email_address: str
    password: str
    age: int
    gender: int
    deactivated: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
