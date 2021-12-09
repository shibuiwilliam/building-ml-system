from typing import Optional

from pydantic import BaseModel, Extra


class UserRequest(BaseModel):
    id: Optional[str]
    handle_name: Optional[str]
    email_address: Optional[str]
    age: Optional[int]
    gender: Optional[int]
    deactivated: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class UserCreateRequest(BaseModel):
    handle_name: Optional[str]
    email_address: Optional[str]
    age: Optional[int]
    gender: Optional[int]

    class Config:
        extra = Extra.forbid
