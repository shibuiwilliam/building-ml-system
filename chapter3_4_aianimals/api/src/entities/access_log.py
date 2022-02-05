from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra


class Action(Enum):
    SELECT = "select"
    SEE_LONG = "see_long"
    LIKE = "like"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in Action.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in Action.__members__.values()]

    @staticmethod
    def value_to_key(value: Optional[str] = None) -> Optional[Enum]:
        if value is None:
            return None
        for v in [v for v in Action.__members__.values()]:
            if value == v.value:
                return v
        return None


class AccessLogCreate(BaseModel):
    id: str
    phrases: List[str]
    animal_category_id: Optional[int] = None
    animal_subcategory_id: Optional[int] = None
    user_id: str
    likes: int
    animal_id: str
    action: Action
    created_at: Optional[datetime]

    class Config:
        extra = Extra.forbid
