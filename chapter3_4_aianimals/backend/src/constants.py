from enum import Enum

from pydantic import BaseModel


class Gender(BaseModel):
    id: int
    name: str


class GENDER(Enum):
    FEMALE = Gender(id=0, name="female")
    MALE = Gender(id=1, name="male")
    OTHER = Gender(id=2, name="other")


class RUN_ENVIRONMENT(Enum):
    LOCAL = "local"
    CLOUD = "cloud"
