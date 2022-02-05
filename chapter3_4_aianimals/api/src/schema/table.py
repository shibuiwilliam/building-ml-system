from enum import Enum


class TABLES(Enum):
    ANIMAL_CATEGORY = "animal_categories"
    ANIMAL_SUBCATEGORY = "animal_subcategories"
    ANIMAL = "animals"
    USER = "users"
    LIKE = "likes"
    VIOLATION_TYPE = "violation_types"
    VIOLATION = "violations"
    ACCESS_LOG = "access_logs"
