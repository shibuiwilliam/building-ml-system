from enum import Enum
from typing import List


class TABLES(Enum):
    ACCESS_LOG = "access_logs"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in TABLES.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in TABLES.__members__.values()]
