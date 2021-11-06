from copy import deepcopy
from typing import Dict, Optional, Union

import mlflow
import numpy as np
import optuna
import pandas as pd
from sklearn.model_selection import BaseCrossValidator
from src.middleware.logger import configure_logger
from src.models.base_model import BaseDemandForecastingModel
from src.optimizer.schema import DIRECTION, METRICS, SUGGEST_TYPE, EvalutionMetrics

logger = configure_logger(name=__name__)


def mlflow_callback(
    study: optuna.Study,
    trial: optuna.Trial,
):
    trial_value = trial.value if trial.value is not None else float("nan")
    with mlflow.start_run(run_name=study.study_name):
        mlflow.log_params(trial.params)
        mlflow.log_param("model", study.study_name)
        mlflow.log_metrics({"accuracy": trial_value})


class Optimizer(object):
    def __init__(
        self,
        data: pd.DataFrame,
        target: pd.DataFrame,
        cv=BaseCrossValidator,
        direction: DIRECTION = DIRECTION.MAXIMIZE,
    ):
        self.data = data
        self.target = target
        self.direction = direction
        self.cv = cv

        optuna.logging.enable_default_handler()

    def optimize(
        self,
        model: BaseDemandForecastingModel,
        n_trials: int = 20,
        n_jobs: int = 1,
        metrics: EvalutionMetrics = METRICS.MEAN_ABSOLUTE_ERROR.value,
        fit_params: Optional[Dict] = None,
    ) -> Dict[str, Union[str, float]]:
        logger.info(f"model: {model}")
        study = optuna.create_study(
            study_name=model.name,
            direction=self.direction.value,
        )
        study.optimize(
            self.objective(
                model=model,
                metrics=metrics,
                fit_params=fit_params,
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
        return result

    def objective(
        self,
        model: BaseDemandForecastingModel,
        metrics: EvalutionMetrics = METRICS.MEAN_ABSOLUTE_ERROR.value,
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

            evaluations = []
            for train_index, test_index in self.cv.split(X=self.data):
                model.reset_model(params=params)
                _model = deepcopy(model.model)
                x_train = self.data.iloc[train_index]
                y_train = self.target.iloc[train_index]
                x_test = self.data.iloc[test_index]
                y_test = self.target.iloc[test_index]
                eval_set = [(x_train, y_train), (x_test, y_test)]

                _model.fit(
                    X=x_train,
                    y=y_train,
                    eval_set=eval_set,
                    **fit_params,
                )
                preds = _model.predict(x_test)
                evaluation = metrics.function(y_test, preds)
                evaluations.append(evaluation)
            return sum(evaluations) / len(evaluations)

        return _objective
