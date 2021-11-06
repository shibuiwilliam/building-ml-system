from enum import Enum
from typing import Any, Callable, Optional

from pydantic import BaseModel
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error


class SUGGEST_TYPE(Enum):
    CATEGORICAL = "categorical"
    INT = "int"
    UNIFORM = "uniform"


class SearchParams(BaseModel):
    name: str
    suggest_type: SUGGEST_TYPE
    value_range: Any


class EvalutionMetrics(BaseModel):
    name: str
    function: Callable


class METRICS(Enum):
    MEAN_ABSOLUTE_ERROR = EvalutionMetrics(
        name="mean_absolute_error",
        function=mean_absolute_error,
    )
    MEAN_ABSOLUTE_PERCENTAGE_ERROR = EvalutionMetrics(
        name="mean_absolute_percentage_error",
        function=mean_absolute_percentage_error,
    )
    MEAN_SQUARED_ERROR = EvalutionMetrics(
        name="mean_squared_error",
        function=mean_squared_error,
    )

    @staticmethod
    def get_metrics(name: str) -> Optional[EvalutionMetrics]:
        for metrics in [v.value for v in METRICS.__members__.values()]:
            if metrics.name == name:
                return metrics
        raise ValueError


class DIRECTION(Enum):
    MINIMIZE = "minimize"
    MAXIMIZE = "maximize"
