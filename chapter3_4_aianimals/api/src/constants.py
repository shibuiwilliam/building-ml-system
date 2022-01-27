from enum import Enum
from typing import List

from pydantic import BaseModel


class Gender(BaseModel):
    id: int
    name: str


class GENDER(Enum):
    FEMALE = Gender(id=0, name="female")
    MALE = Gender(id=1, name="male")
    OTHER = Gender(id=2, name="other")

    @staticmethod
    def has_id(id: int) -> bool:
        return id in [v.value.id for v in GENDER.__members__.values()]

    @staticmethod
    def has_name(name: str) -> bool:
        return name in [v.value.name for v in GENDER.__members__.values()]

    @staticmethod
    def get_list() -> List[Gender]:
        return [v.value for v in GENDER.__members__.values()]


class RUN_ENVIRONMENT(Enum):
    LOCAL = "local"
    CLOUD = "cloud"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in RUN_ENVIRONMENT.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in RUN_ENVIRONMENT.__members__.values()]


def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()

    return property(fget, fset)


class _CONSTANTS(object):
    @constant
    def TOKEN() -> str:
        return "token"

    @constant
    def TOKEN_SPLITTER() -> str:
        return "____"

    @constant
    def ANIMAL_SEARCH_CACHE_PREFIX() -> str:
        return "ANIMAL_SEARCH_CACHE"


CONSTANTS = _CONSTANTS()
