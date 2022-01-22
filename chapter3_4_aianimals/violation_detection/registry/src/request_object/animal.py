from pydantic import BaseModel, Extra


class AnimalUpdateRequest(BaseModel):
    id: str
    deactivated: bool

    class Config:
        extra = Extra.forbid
