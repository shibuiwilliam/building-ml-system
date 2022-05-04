from enum import Enum
from typing import List


class RUN_ENVIRONMENT(Enum):
    LOCAL = "local"
    CLOUD = "cloud"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in RUN_ENVIRONMENT.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in RUN_ENVIRONMENT.__members__.values()]


class _CONSTANTS(object):
    @constant
    def SPLITTER() -> str:
        return "____"


CONSTANTS = _CONSTANTS()
