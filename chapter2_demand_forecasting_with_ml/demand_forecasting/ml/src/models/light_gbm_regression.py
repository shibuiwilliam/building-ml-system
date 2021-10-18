from collections import OrderedDict
from typing import Any, Dict, List, Optional, Union

import lightgbm as lgb
import numpy as np
import onnxmltools
import pandas as pd
import yaml
from lightgbm import LGBMRegressor
from onnxmltools.convert.common.data_types import DoubleTensorType
from src.models.base_model import SUGGEST_TYPE, BaseDemandForecastingModel, SearchParams
from src.utils.logger import configure_logger

logger = configure_logger(__name__)

DEFAULT_PARAMS = {
    "task": "train",
    "boosting": "gbdt",
    "objective": "regression",
    "metric": ["mse"],
    "num_leaves": 3,
    "learning_rate": 0.01,
    "feature_fraction": 0.8,
    "max_depth": -1,
    "verbose": 0,
    "num_boost_round": 200000,
    "early_stopping_rounds": 200,
    "num_threads": 0,
    "seed": 1234,
}


class LightGBMRegressionDemandForecasting(BaseDemandForecastingModel):
    def __init__(
        self,
        params: Dict = DEFAULT_PARAMS,
        early_stopping_rounds: int = 200,
        verbose_eval: int = 100,
    ):
        self.name = "light_gbm_regression"
        self.params = params
        self.early_stopping_rounds = early_stopping_rounds
        self.verbose_eval = verbose_eval
        self.model: LGBMRegressor = LGBMRegressor(**self.params)
        self.search_params: List[SearchParams] = []
        self.column_length: int = 0

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
        logger.info(f"start train with params: {self.params}")
        eval_set = [(x_train, y_train)]
        if x_test is not None and y_test is not None:
            eval_set.append((x_test, y_test))
        self.model.fit(
            X=x_train,
            y=y_train,
            eval_set=eval_set,
            early_stopping_rounds=self.early_stopping_rounds,
            eval_metric=["mse"],
            verbose=self.verbose_eval,
        )

    def predict(
        self,
        x_test: Union[np.ndarray, pd.DataFrame],
    ) -> Union[np.ndarray, pd.DataFrame]:
        predictions = self.model.predict(x_test)
        return predictions

    def save_model_params(
        self,
        file_path: str,
    ):
        logger.info(f"save model params: {file_path}")
        with open(file_path, "w") as f:
            yaml.dump(self.params, f)

    def save(
        self,
        file_path: str,
    ):
        logger.info(f"save model: {file_path}")
        self.model.booster_.save_model(file_path)

    def load(
        self,
        file_path: str,
    ):
        logger.info(f"load model: {file_path}")
        self.model = lgb.Booster(model_file=file_path)

    def save_as_onnx(
        self,
        file_path: str,
    ):
        logger.info(f"save model as onnx: {file_path}")
        initial_types = [["inputs", DoubleTensorType([None, self.column_length])]]
        onnx_model = onnxmltools.convert_lightgbm(self.model, initial_types=initial_types)
        onnxmltools.utils.save_model(onnx_model, file_path)
