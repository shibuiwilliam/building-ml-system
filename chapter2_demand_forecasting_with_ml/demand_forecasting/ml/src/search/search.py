from enum import Enum
from typing import Dict, Iterator, List, Optional, Union

import mlflow
import numpy as np
import optuna
import pandas as pd
from omegaconf import DictConfig
from sklearn.model_selection import BaseCrossValidator, cross_validate
from src.models.base_model import BaseDemandForecastingModel
from src.search.schema import SUGGEST_TYPE, SearchParams
from src.utils.logger import configure_logger

logger = configure_logger(name=__name__)


def parse_params(params: DictConfig) -> List[SearchParams]:
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


class DIRECTION(Enum):
    MINIMIZE = "minimize"
    MAXIMIZE = "maximize"


def mlflow_callback(
    study: optuna.Study,
    trial: optuna.Trial,
):
    trial_value = trial.value if trial.value is not None else float("nan")
    with mlflow.start_run(run_name=study.study_name):
        mlflow.log_params(trial.params)
        mlflow.log_param("model", study.study_name)
        mlflow.log_metrics({"accuracy": trial_value})


class OptunaRunner(object):
    def __init__(
        self,
        data: pd.DataFrame,
        target: pd.DataFrame,
        direction: DIRECTION = DIRECTION.MAXIMIZE,
        cv: Union[int, BaseCrossValidator] = 5,
        scorings: Optional[Dict[str, str]] = None,
    ):
        self.data = data
        self.target = target
        self.direction = direction
        self.cv = cv
        self.scorings = scorings
        if self.scorings is None:
            self.scorings = {
                "neg_root_mean_squared_error": "neg_root_mean_squared_error",
                "neg_mean_absolute_error": "neg_mean_absolute_error",
                "neg_mean_absolute_percentage_error": "neg_mean_absolute_percentage_error",
            }

        optuna.logging.enable_default_handler()

    def optimize(
        self,
        models: List[BaseDemandForecastingModel],
        n_trials: int = 20,
        n_jobs: int = 1,
        scoring: str = "test_neg_mean_absolute_error",
        fit_params: Optional[Dict] = None,
    ) -> List[Dict[str, Union[str, float]]]:
        return list(
            self._optimize(
                models=models,
                n_jobs=n_jobs,
                n_trials=n_trials,
                fit_params=fit_params,
                scoring=scoring,
            )
        )

    def _optimize(
        self,
        models: List[BaseDemandForecastingModel],
        n_trials: int = 20,
        n_jobs: int = 1,
        scoring: str = "test_neg_mean_absolute_error",
        fit_params: Optional[Dict] = None,
    ) -> Iterator[Dict[str, Union[str, float]]]:
        for model in models:
            logger.info(f"model: {model}")
            study = optuna.create_study(
                study_name=model.name,
                direction=self.direction.value,
            )
            study.optimize(
                self.objective(
                    model=model,
                    fit_params=fit_params,
                    scoring=scoring,
                ),
                n_jobs=n_jobs,
                n_trials=n_trials,
                callbacks=[mlflow_callback],
            )
            result = {
                "model": model.name,
                "best_score": study.best_value,
                "best_params": study.best_params,
            }
            logger.info(f"result for {model.name}: {result}")
            yield result

    def objective(
        self,
        model: BaseDemandForecastingModel,
        scoring: str = "test_neg_mean_absolute_error",
        fit_params: Optional[Dict] = None,
    ):
        def _objective(
            trial: optuna.Trial,
        ) -> float:

            params = {}
            for search_param in model.search_params:
                if search_param.suggest_type == SUGGEST_TYPE.CATEGORICAL:
                    params[search_param.name] = trial.suggest_categorical(
                        search_param.name,
                        search_param.value_range,
                    )
                elif search_param.suggest_type == SUGGEST_TYPE.INT:
                    params[search_param.name] = trial.suggest_int(
                        search_param.name,
                        search_param.value_range[0],
                        search_param.value_range[1],
                    )
                elif search_param.suggest_type == SUGGEST_TYPE.UNIFORM:
                    params[search_param.name] = trial.suggest_uniform(
                        search_param.name,
                        search_param.value_range[0],
                        search_param.value_range[1],
                    )

            logger.info(f"params: {params}")

            scores = cross_validate(
                estimator=model.model,
                X=self.data,
                y=self.target,
                cv=self.cv,
                scoring=self.scorings,
                error_score=np.nan,
                fit_params=fit_params,
            )
            logger.debug(f"result: {scores}")
            return scores[scoring].mean()

        return _objective
