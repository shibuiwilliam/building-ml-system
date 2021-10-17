from enum import Enum
from typing import Dict, Iterator, List, Union

import mlflow
import numpy as np
import optuna
import pandas as pd
from sklearn.model_selection import cross_validate
from src.models.base_model import SUGGEST_TYPE, BaseDemandForecastingModel
from src.utils.logger import configure_logger

logger = configure_logger(name=__name__)


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
        cv: int = 5,
        scorings: Dict[str, str] = {
            "accuracy": "accuracy",
            "precision_macro": "precision_macro",
            "recall_macro": "recall_macro",
        },
    ):
        self.data = data
        self.target = target
        self.direction = direction
        self.cv = cv
        self.scorings = scorings

        optuna.logging.enable_default_handler()

    def optimize(
        self,
        estimators: List[BaseDemandForecastingModel],
        n_trials: int = 20,
        n_jobs: int = 1,
    ) -> List[Dict[str, Union[str, float]]]:
        return list(
            self._optimize(
                estimators=estimators,
                n_jobs=n_jobs,
                n_trials=n_trials,
            )
        )

    def _optimize(
        self,
        estimators: List[BaseDemandForecastingModel],
        n_trials: int = 20,
        n_jobs: int = 1,
    ) -> Iterator[Dict[str, Union[str, float]]]:
        for estimator in estimators:
            logger.info(f"estimator: {estimator}")
            study = optuna.create_study(
                study_name=estimator.name,
                direction=self.direction.value,
            )
            study.optimize(
                self.objective(estimator=estimator),
                n_jobs=n_jobs,
                n_trials=n_trials,
                callbacks=[mlflow_callback],
            )
            result = {
                "estimator": estimator.name,
                "best_score": study.best_value,
                "best_params": study.best_params,
            }
            logger.info(f"result for {estimator.name}: {result}")
            yield result

    def objective(
        self,
        estimator: BaseDemandForecastingModel,
    ):
        def _objective(
            trial: optuna.Trial,
        ) -> float:

            params = {}
            for search_param in estimator.search_params:
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

            logger.debug(f"params: {params}")

            scores = cross_validate(
                estimator=estimator.model,
                X=self.data,
                y=self.target,
                cv=self.cv,
                scoring=self.scorings,
                error_score=np.nan,
            )
            logger.debug(f"result: {scores}")
            return scores["test_accuracy"].mean()

        return _objective
