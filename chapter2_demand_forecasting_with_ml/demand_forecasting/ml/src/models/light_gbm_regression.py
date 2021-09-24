import random
from collections import OrderedDict
from typing import Any, Dict, Union

import lightgbm as lgb
import numpy as np
import onnxmltools
import pandas as pd
import scipy
from onnxmltools.convert.common.data_types import FloatTensorType
from src.models.base_model import BaseDemandForecastingModel
from src.models.preprocess import Expm1Transformer
from src.utils.logger import configure_logger

logger = configure_logger(__name__)

DEFAULT_PARAMS = {
    "task": "train",
    "boosting": "gbdt",
    "objective": "regression",
    "metric": {"mse"},
    "num_leaves": 3,
    "learning_rate": 0.01,
    "feature_fraction": 0.8,
    "max_depth": -1,
    "verbose": 0,
    "num_boost_round": 20000,
    "early_stopping_rounds": 200,
    "num_threads": 0,
    "seed": random.randint(0, 9999),
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
        x_train: Union[np.ndarray, scipy.sparse.csr.csr_matrix, pd.DataFrame],
        x_test: Union[np.ndarray, scipy.sparse.csr.csr_matrix, pd.DataFrame],
        y_train: Union[np.ndarray, scipy.sparse.csr.csr_matrix, pd.DataFrame],
        y_test: Union[np.ndarray, scipy.sparse.csr.csr_matrix, pd.DataFrame],
        verbose_eval: int = 100,
    ):
        lgbtrain = lgb.Dataset(
            data=x_train,
            label=y_train,
        )
        lgbval = lgb.Dataset(
            data=x_test,
            label=y_test,
            reference=lgbtrain,
        )

        self.column_length = x_train.shape[1]
        evals_result: Dict[OrderedDict, Any] = {}
        self.model = lgb.train(
            self.params,
            lgbtrain,
            num_boost_round=self.params["num_boost_round"],
            valid_sets=[lgbtrain, lgbval],
            early_stopping_rounds=self.params["early_stopping_rounds"],
            evals_result=evals_result,
            verbose_eval=verbose_eval,
        )
        logger.info(
            f"""
Train history:
{evals_result}
        """
        )

    def predict(
        self,
        x_test: Union[np.ndarray, scipy.sparse.csr.csr_matrix, pd.DataFrame],
    ) -> np.ndarray:
        log1p_predictions = self.model.predict(x_test)
        predictions = Expm1Transformer().fit_transform(log1p_predictions)
        return predictions

    def save(
        self,
        file_path: str,
    ):
        self.model.save_model(file_path)

    def save_as_onnx(
        self,
        file_path: str,
    ):
        initial_types = [["inputs", FloatTensorType([None, self.column_length])]]
        onnx_model = onnxmltools.convert_lightgbm(self.model, initial_types=initial_types)
        onnxmltools.utils.save_model(onnx_model, file_path)
