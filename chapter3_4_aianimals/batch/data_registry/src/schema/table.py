from enum import Enum
from typing import List


class TABLES(Enum):
    ANIMAL_CATEGORY = "animal_categories"
    ANIMAL_SUBCATEGORY = "animal_subcategories"
    ANIMAL = "animals"
    USER = "users"
    LIKE = "likes"
    VIOLATION_TYPE = "violation_types"
    VIOLATION = "violations"
    ACCESS_LOG = "access_logs"
    ANIMAL_FEATURE = "animal_features"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in TABLES.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in TABLES.__members__.values()]
