from typing import Dict, List, Optional

from pydantic import BaseModel, Extra
from src.configurations import Configurations


class AnimalRequest(BaseModel):
    id: str

    class Config:
        extra = Extra.forbid


class AnimalResponse(BaseModel):
    ids: List[str]
    model_name: Optional[str] = Configurations.model_name

    class Config:
        extra = Extra.forbid


class AnimalRequestResponse(BaseModel):
    request: Dict[str, str] = dict(id="str")
    response: Dict[str, List[str]] = dict(ids=["str"])
