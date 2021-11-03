import os
from typing import Dict, List, Optional, Union

import lightgbm as lgb
import numpy as np
import onnxmltools
import pandas as pd
import yaml
from lightgbm import LGBMRegressor
from onnxmltools.convert.common.data_types import DoubleTensorType
from src.models.base_model import BaseDemandForecastingModel
from src.search.schema import SUGGEST_TYPE, SearchParams
from src.utils.logger import configure_logger

logger = configure_logger(__name__)

LGB_REGRESSION_DEFAULT_PARAMS = {
    "task": "train",
    "boosting": "gbdt",
    "objective": "regression",
    "num_leaves": 4,
    "learning_rate": 0.01,
    "feature_fraction": 0.8,
    "max_depth": -1,
    "num_iterations": 1000000,
    "num_threads": 1,
    "seed": 1234,
}


class LightGBMRegressionDemandForecasting(BaseDemandForecastingModel):
    def __init__(
        self,
        params: Dict = LGB_REGRESSION_DEFAULT_PARAMS,
        early_stopping_rounds: int = 200,
        eval_metrics: Union[str, List[str]] = "mse",
        verbose_eval: int = 1000,
    ):
        self.name = "light_gbm_regression"
        self.params = params
        self.early_stopping_rounds = early_stopping_rounds
        self.eval_metrics = eval_metrics
        self.verbose_eval = verbose_eval

        self.model: LGBMRegressor = None
        self.reset_model(params=self.params)
        self.search_params: List[SearchParams] = []
        self.column_length: int = 0

    def reset_model(
        self,
        params: Optional[Dict] = None,
    ):
        if params is not None:
            self.params = params
        logger.info(f"params: {self.params}")
        self.model = LGBMRegressor(**self.params)
        logger.info(f"initialized model: {self.model}")

    def define_default_search_params(self):
        self.search_params = [
            SearchParams(
                name="num_leaves",
                suggest_type=SUGGEST_TYPE.INT,
                value_range=(2, 100),
            ),
            SearchParams(
                name="max_depth",
                suggest_type=SUGGEST_TYPE.INT,
                value_range=(2, 100),
            ),
            SearchParams(
                name="learning_rate",
                suggest_type=SUGGEST_TYPE.UNIFORM,
                value_range=[0.0001, 0.01],
            ),
            SearchParams(
                name="feature_fraction",
                suggest_type=SUGGEST_TYPE.UNIFORM,
                value_range=[0.001, 0.9],
            ),
        ]

    def define_search_params(
        self,
        search_params: List[SearchParams],
    ):
        self.search_params = search_params

    def train(
        self,
        x_train: Union[np.ndarray, pd.DataFrame],
        y_train: Union[np.ndarray, pd.DataFrame],
        x_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        y_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
    ):
        logger.info(f"start train for model: {self.model}")
        eval_set = [(x_train, y_train)]
        if x_test is not None and y_test is not None:
            eval_set.append((x_test, y_test))
        self.model.fit(
            X=x_train,
            y=y_train,
            eval_set=eval_set,
            early_stopping_rounds=self.early_stopping_rounds,
            eval_metric=self.eval_metrics,
            verbose=self.verbose_eval,
        )

    def predict(
        self,
        x: Union[np.ndarray, pd.DataFrame],
    ) -> Union[np.ndarray, pd.DataFrame]:
        predictions = self.model.predict(x)
        return predictions

    def save_model_params(
        self,
        file_path: str,
    ) -> str:
        file, ext = os.path.splitext(file_path)
        if ext != ".yaml":
            file_path = f"{file}.yaml"
        logger.info(f"save model params: {file_path}")
        with open(file_path, "w") as f:
            yaml.dump(self.params, f)
        return file_path

    def save(
        self,
        file_path: str,
    ) -> str:
        file, ext = os.path.splitext(file_path)
        if ext != ".txt":
            file_path = f"{file}.txt"
        logger.info(f"save model: {file_path}")
        self.model.booster_.save_model(file_path)
        return file_path

    def load(
        self,
        file_path: str,
    ):
        logger.info(f"load model: {file_path}")
        self.model = lgb.Booster(model_file=file_path)

    def save_as_onnx(
        self,
        file_path: str,
    ) -> str:
        file, ext = os.path.splitext(file_path)
        if ext != ".onnx":
            file_path = f"{file}.onnx"
        logger.info(f"save model as onnx: {file_path}")
        initial_types = [["inputs", DoubleTensorType([None, self.column_length])]]
        onnx_model = onnxmltools.convert_lightgbm(self.model, initial_types=initial_types)
        onnxmltools.utils.save_model(onnx_model, file_path)
        return file_path
