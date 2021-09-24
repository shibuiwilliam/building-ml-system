import json
from collections import OrderedDict
from typing import Any, Dict, Optional, Union

import lightgbm as lgb
import numpy as np
import onnxmltools
import pandas as pd
from onnxmltools.convert.common.data_types import FloatTensorType
from src.models.base_model import BaseDemandForecastingModel
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
    ):
        self.params = params
        self.model: lgb.basic.Booster = None
        self.column_length: int = 0
        self.name = "light_gbm_regression"

    def train(
        self,
        x_train: Union[np.ndarray, pd.DataFrame],
        y_train: Union[np.ndarray, pd.DataFrame],
        x_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        y_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        verbose_eval: int = 100,
    ) -> Dict[OrderedDict, Any]:
        logger.info(f"start train with params: {self.params}")
        lgbtrain = lgb.Dataset(
            data=x_train,
            label=y_train,
        )
        valid_sets = [lgbtrain]
        if x_test is not None and y_test is not None:
            lgbval = lgb.Dataset(
                data=x_test,
                label=y_test,
                reference=lgbtrain,
            )
            valid_sets.append(lgbval)

        self.column_length = x_train.shape[1]
        evals_result: Dict[OrderedDict, Any] = {}
        self.model = lgb.train(
            self.params,
            lgbtrain,
            num_boost_round=self.params["num_boost_round"],
            valid_sets=valid_sets,
            early_stopping_rounds=self.params["early_stopping_rounds"],
            evals_result=evals_result,
            verbose_eval=verbose_eval,
        )
        return evals_result

    def predict(
        self,
        x_test: Union[np.ndarray, pd.DataFrame],
    ) -> np.ndarray:
        predictions = self.model.predict(x_test)
        return predictions

    def save_model_params(
        self,
        file_path: str,
    ):
        logger.info(f"save model params: {file_path}")
        with open(file_path, "w") as f:
            json.dump(self.params, f)

    def save_train_history(
        self,
        evals_result: Dict[OrderedDict, Any],
        file_path: str,
    ):
        logger.info(f"save train history: {file_path}")
        with open(file_path, "w") as f:
            json.dump(evals_result, f)

    def save(
        self,
        file_path: str,
    ):
        logger.info(f"save model: {file_path}")
        self.model.save_model(file_path)

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
        initial_types = [["inputs", FloatTensorType([None, self.column_length])]]
        onnx_model = onnxmltools.convert_lightgbm(self.model, initial_types=initial_types)
        onnxmltools.utils.save_model(onnx_model, file_path)
