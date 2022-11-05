from typing import List

from pydantic import BaseModel, Extra


class AccessLog(BaseModel):
    phrases: List[str]

    class Config:
        extra = Extra.forbid
