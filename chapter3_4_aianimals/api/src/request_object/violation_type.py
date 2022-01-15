from typing import Optional

from pydantic import BaseModel, Extra


class ViolationTypeRequest(BaseModel):
    id: Optional[str]
    name: Optional[str]

    class Config:
        extra = Extra.forbid


class ViolationTypeCreateRequest(BaseModel):
    name: str

    class Config:
        extra = Extra.forbid
