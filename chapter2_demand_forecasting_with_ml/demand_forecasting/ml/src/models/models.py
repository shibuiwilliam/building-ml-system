import dataclasses
from enum import Enum
from typing import Dict, List, Optional

from src.models.base_model import BaseDemandForecastingModel
from src.models.light_gbm_regression import DEFAULT_PARAMS, LightGBMRegressionDemandForecasting


@dataclasses.dataclass(frozen=True)
class Model(object):
    name: str
    model: BaseDemandForecastingModel
    params: Dict


class MODELS(Enum):
    LIGHT_GBM_REGRESSION = Model(
        name="light_gbm_regression",
        model=LightGBMRegressionDemandForecasting,
        params=DEFAULT_PARAMS,
    )

    @staticmethod
    def has_value(name: str) -> bool:
        return name in [v.value.name for v in MODELS.__members__.values()]

    @staticmethod
    def get_list() -> List[Model]:
        return [v.value for v in MODELS.__members__.values()]

    @staticmethod
    def get_value(name: str) -> Optional[Model]:
        for model in [v.value for v in MODELS.__members__.values()]:
            if model.name == name:
                return model
        return None
