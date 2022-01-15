from enum import Enum
from typing import List

from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class TABLES(Enum):
    ANIMAL_CATEGORY = "animal_categories"
    ANIMAL_SUBCATEGORY = "animal_subcategories"
    ANIMAL = "animals"
    USER = "users"
    LIKE = "likes"
    VIOLATION_TYPE = "violation_types"
    VIOLATION = "violations"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in TABLES.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in TABLES.__members__.values()]
