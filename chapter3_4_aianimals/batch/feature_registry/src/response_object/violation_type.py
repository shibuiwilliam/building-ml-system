from datetime import datetime

from pydantic import BaseModel, Extra


class ViolationTypeResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
