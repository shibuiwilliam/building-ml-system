from enum import Enum
from typing import Any

from pydantic import BaseModel


class SUGGEST_TYPE(Enum):
    CATEGORICAL = "categorical"
    INT = "int"
    UNIFORM = "uniform"


class SearchParams(BaseModel):
    name: str
    suggest_type: SUGGEST_TYPE
    value_range: Any
