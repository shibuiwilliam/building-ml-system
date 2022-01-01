from datetime import datetime

from pydantic import BaseModel, Extra


class UserResponse(BaseModel):
    id: str
    handle_name: str
    email_address: str
    age: int
    gender: int
    deactivated: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class UserLoginResponse(BaseModel):
    token: str
