import dataclasses
from enum import Enum
from typing import Dict, List

from src.models.lightgbm_ranker import LIGHT_GBM_LEARN_TO_RANK_RANKER, LightGBMLearnToRankRanker
from src.models.lightgbm_regression import LIGHT_GBM_LEARN_TO_RANK_REGRESSION, LightGBMLearnToRankRegression


@dataclasses.dataclass(frozen=True)
class Model(object):
    name: str
    model: type
    params: Dict


class MODELS(Enum):
    LIGHT_GBM_LEARN_TO_RANK_REGRESSION = Model(
        name="learn_to_rank_lightgbm_regression",
        model=LightGBMLearnToRankRegression,
        params=LIGHT_GBM_LEARN_TO_RANK_REGRESSION,
    )
    LIGHT_GBM_LEARN_TO_RANK_RANKER = Model(
        name="learn_to_rank_lightgbm_ranker",
        model=LightGBMLearnToRankRanker,
        params=LIGHT_GBM_LEARN_TO_RANK_RANKER,
    )

    @staticmethod
    def has_value(name: str) -> bool:
        return name in [v.value.name for v in MODELS.__members__.values()]

    @staticmethod
    def get_list() -> List[Model]:
        return [v.value for v in MODELS.__members__.values()]

    @staticmethod
    def get_model(name: str) -> Model:
        for model in [v.value for v in MODELS.__members__.values()]:
            if model.name == name:
                return model
        raise ValueError("invalid model name")
