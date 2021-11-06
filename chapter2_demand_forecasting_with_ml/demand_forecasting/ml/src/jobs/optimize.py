from typing import Any, Dict, List, Optional

from omegaconf import DictConfig
from src.middleware.logger import configure_logger
from src.models.base_model import BaseDemandForecastingModel
from src.optimizer.optimizer import Optimizer
from src.optimizer.schema import SUGGEST_TYPE, SearchParams

logger = configure_logger(name=__name__)


class OptimizerRunner(object):
    def __init__(
        self,
        model: BaseDemandForecastingModel,
        optimizer: Optimizer,
    ):
        self.model = model
        self.optimizer = optimizer

    def optimize(
        self,
        params: DictConfig,
        scoring: str = "test_neg_mean_squared_error",
        n_trials: int = 20,
        n_jobs: int = 1,
        fit_params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        search_params = self.parse_params(params=params)
        self.model.define_search_params(search_params=search_params)
        result = self.optimizer.optimize(
            model=self.model,
            n_trials=n_trials,
            n_jobs=n_jobs,
            scoring=scoring,
            fit_params=fit_params,
        )

        logger.info(f"parameter search result: {result}")
        best_params = result["best_params"]
        for k, v in self.model.params.items():
            if k not in best_params.keys():
                best_params[k] = v
        return best_params

    def parse_params(
        self,
        params: DictConfig,
    ) -> List[SearchParams]:
        search_params = []
        for param in params:
            if param.suggest_type == SUGGEST_TYPE.CATEGORICAL.value:
                search_params.append(
                    SearchParams(
                        name=param.name,
                        suggest_type=SUGGEST_TYPE.CATEGORICAL,
                        value_range=param.value_range,
                    )
                )
            elif param.suggest_type == SUGGEST_TYPE.INT.value:
                search_params.append(
                    SearchParams(
                        name=param.name,
                        suggest_type=SUGGEST_TYPE.INT,
                        value_range=tuple(param.value_range),
                    )
                )
            elif param.suggest_type == SUGGEST_TYPE.UNIFORM.value:
                search_params.append(
                    SearchParams(
                        name=param.name,
                        suggest_type=SUGGEST_TYPE.UNIFORM,
                        value_range=tuple(param.value_range),
                    )
                )

        logger.info(f"params: {search_params}")
        return search_params
