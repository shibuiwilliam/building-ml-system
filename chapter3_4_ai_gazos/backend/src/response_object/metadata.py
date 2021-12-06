from typing import List

from pydantic import BaseModel, Extra
from src.constants import Gender


class MetadataResponse(BaseModel):
    gender: List[Gender]

    class Config:
        extra = Extra.forbid
