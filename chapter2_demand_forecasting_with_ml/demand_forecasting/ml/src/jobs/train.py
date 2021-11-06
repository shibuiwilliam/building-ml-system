from typing import Optional, Union

import mlflow
import numpy as np
import pandas as pd
from pydantic import BaseModel
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
from src.middleware.logger import configure_logger
from src.models.base_model import BaseDemandForecastingModel

logger = configure_logger(name=__name__)


class Evaluation(BaseModel):
    mean_absolute_error: float
    mean_absolute_percentage_error: float
    root_mean_squared_error: float


class Trainer(object):
    def __init__(self):
        pass

    def train(
        self,
        model: BaseDemandForecastingModel,
        x_train: Union[np.ndarray, pd.DataFrame],
        y_train: Union[np.ndarray, pd.DataFrame],
        x_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        y_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
    ):
        model.train(
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
        )

    def evaluate(
        self,
        model: BaseDemandForecastingModel,
        x: Union[np.ndarray, pd.DataFrame],
        y: Union[np.ndarray, pd.DataFrame],
    ) -> Evaluation:
        predictions = model.predict(x=x)
        rmse = mean_squared_error(
            y_true=y,
            y_pred=predictions,
            squared=False,
        )
        mae = mean_absolute_error(
            y_true=y,
            y_pred=predictions,
        )
        mape = mean_absolute_percentage_error(
            y_true=y,
            y_pred=predictions,
        )
        evaluation = Evaluation(
            mean_absolute_error=mae,
            mean_absolute_percentage_error=mape,
            root_mean_squared_error=rmse,
        )
        logger.info(
            f"""
model: {model.name}
mae: {evaluation.mean_absolute_error}
mape: {evaluation.mean_absolute_percentage_error}
rmse: {evaluation.root_mean_squared_error}
            """
        )
        return evaluation

    def train_and_evaluate(
        self,
        model: BaseDemandForecastingModel,
        x_train: Union[np.ndarray, pd.DataFrame],
        y_train: Union[np.ndarray, pd.DataFrame],
        x_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        y_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        save_file_path: Optional[str] = None,
        onnx_file_path: Optional[str] = None,
    ) -> Evaluation:
        logger.info("start training and evaluation")
        with mlflow.start_run(run_name=model.name):
            self.train(
                model=model,
                x_train=x_train,
                y_train=y_train,
                x_test=x_test,
                y_test=y_test,
            )
            evaluation = self.evaluate(
                model=model,
                x=x_test,
                y=y_test,
            )
            mlflow.log_param("model", model.name)
            mlflow.log_params(model.params)
            mlflow.log_metrics(evaluation.dict())

            if save_file_path is not None:
                f = model.save(file_path=save_file_path)
                mlflow.log_artifact(f)

            if onnx_file_path is not None:
                f = model.save_as_onnx(file_path=onnx_file_path)
                mlflow.log_artifact(f)

        logger.info("done training and evaluation")
        return evaluation
