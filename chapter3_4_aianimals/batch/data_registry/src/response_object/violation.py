from datetime import datetime

from pydantic import BaseModel, Extra


class ViolationResponse(BaseModel):
    id: str
    animal_id: str
    violation_type_id: str
    probability: float
    judge: str
    is_effective: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid
