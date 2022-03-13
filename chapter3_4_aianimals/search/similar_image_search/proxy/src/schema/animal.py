from typing import List, Dict, Optional

from pydantic import BaseModel, Extra


class AnimalRequest(BaseModel):
    id: str

    class Config:
        extra = Extra.forbid


class AnimalResponse(BaseModel):
    ids: List[str]

    class Config:
        extra = Extra.forbid


class AnimalRequestResponse(BaseModel):
    request: Dict[str, str] = dict(id="str")
    response: Dict[str, List[str]] = dict(ids=["str"])
