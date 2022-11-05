from typing import Optional

from pydantic import BaseModel, Extra


class ViolationRequest(BaseModel):
    id: Optional[str]
    animal_id: Optional[str]
    violation_type_id: Optional[str]
    probability_lower_bound: Optional[float]
    probability_upper_bound: Optional[float]
    judge: Optional[str]
    is_effective: Optional[bool]
    is_administrator_checked: Optional[bool]

    class Config:
        extra = Extra.forbid


class ViolationCreateRequest(BaseModel):
    id: str
    animal_id: str
    violation_type_id: str
    probability: float
    judge: str
    is_effective: bool
    is_administrator_checked: bool

    class Config:
        extra = Extra.forbid
