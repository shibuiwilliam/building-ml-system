from pydantic import BaseModel, Extra


class ViolationCreateRequest(BaseModel):
    animal_id: str
    violation_type_id: str
    probability: float
    judge: str
    is_effective: bool

    class Config:
        extra = Extra.forbid
