from typing import Optional, Tuple, Union

import numpy as np
import pandas as pd
from pydantic import BaseModel
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
from src.middleware.logger import configure_logger
from src.models.base_model import BaseDemandForecastingModel
from src.models.preprocess import DataPreprocessPipeline

logger = configure_logger(name=__name__)


class Evaluation(BaseModel):
    mean_absolute_error: float
    mean_absolute_percentage_error: float
    root_mean_squared_error: float


class Artifact(BaseModel):
    preprocess_file_path: Optional[str]
    model_file_path: Optional[str]
    onnx_file_path: Optional[str]


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
        eval_df = pd.DataFrame({"y_true": y.sales, "y_pred": predictions})
        eval_df["diff"] = eval_df["y_true"] - eval_df["y_pred"]
        eval_df["error_rate"] = eval_df["diff"] / eval_df["y_true"]
        logger.info(f"{eval_df}")

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
        data_preprocess_pipeline: Optional[DataPreprocessPipeline] = None,
        preprocess_pipeline_file_path: Optional[str] = None,
        save_file_path: Optional[str] = None,
        onnx_file_path: Optional[str] = None,
    ) -> Tuple[Evaluation, Artifact]:
        logger.info("start training and evaluation")
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

        artifact = Artifact()
        if data_preprocess_pipeline is not None and preprocess_pipeline_file_path is not None:
            artifact.preprocess_file_path = data_preprocess_pipeline.dump_pipeline(
                file_path=preprocess_pipeline_file_path
            )

        if save_file_path is not None:
            artifact.model_file_path = model.save(file_path=save_file_path)

        if onnx_file_path is not None:
            artifact.onnx_file_path = model.save_as_onnx(file_path=onnx_file_path)

        logger.info("done training and evaluation")
        return evaluation, artifact
