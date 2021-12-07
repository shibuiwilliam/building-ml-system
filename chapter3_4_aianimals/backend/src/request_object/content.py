import json
from typing import Optional

from pydantic import BaseModel, Extra


class ContentRequest(BaseModel):
    id: Optional[str]
    name: Optional[str]
    user_id: Optional[str]
    deactivated: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class ContentCreateRequest(BaseModel):
    user_id: str
    name: str
    description: str

    class Config:
        extra = Extra.forbid

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value