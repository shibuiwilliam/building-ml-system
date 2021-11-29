from datetime import datetime
from typing import Optional

from src.schema.abstract_schema import AbstractCreate, AbstractModel, AbstractQuery


class UserQuery(AbstractQuery):
    id: Optional[str]
    handle_name: Optional[str]
    email_address: Optional[str]
    age: Optional[int]
    gender: Optional[int]
    deactivated: Optional[bool] = False


class UserCreate(AbstractCreate):
    id: str
    handle_name: Optional[str]
    email_address: Optional[str]
    age: Optional[int]
    gender: Optional[int]


class UserModel(AbstractModel):
    id: str
    name: str
    handle_name: str
    email_address: str
    age: int
    gender: int
    deactivated: bool
    created_at: datetime
    updated_at: datetime
