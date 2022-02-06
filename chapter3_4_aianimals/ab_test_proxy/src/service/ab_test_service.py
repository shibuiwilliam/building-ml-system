from enum import Enum
from logging import getLogger
from typing import List, Optional

from pydantic import BaseModel

logger = getLogger(__name__)


class ABTestType(Enum):
    RANDOM = "random"
    USER = "user"
    ANIMAL = "animal"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in ABTestType.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in ABTestType.__members__.values()]

    @staticmethod
    def value_to_key(value: Optional[str] = None) -> Optional[Enum]:
        if value is None:
            return None
        for v in [v for v in ABTestType.__members__.values()]:
            if value == v.value:
                return v
        return None


class Endpoint(BaseModel):
    name: Optional[str]
    endpoint: str
