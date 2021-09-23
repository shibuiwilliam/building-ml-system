import random
from collections import OrderedDict
from typing import Any, Dict, List, Union

import lightgbm as lgb
import numpy as np
import onnxmltools
import pandas as pd
import scipy
from onnxmltools.convert.common.data_types import FloatTensorType
from src.models.preprocess import Expm1Transformer

DEFAULT_PARAMS = {
    "task": "train",
    "boosting": "gbdt",
    "objective": "regression",
    "metric": {"mse"},
    "num_leaves": 10,
    "learning_rate": 0.01,
    "feature_fraction": 0.8,
    "max_depth": -1,
    "verbose": 0,
    "num_boost_round": 20000,
    "early_stopping_rounds": 200,
    "num_threads": 0,
    "seed": random.randint(0, 9999),
}


class LightGBMRegressionDemandForecasting(object):
    def __init__(
        self,
        params: Dict = DEFAULT_PARAMS,
    ):
        self.params = params
        self.model: lgb.basic.Booster = None
        self.column_length: int = 0

    def train(
        self,
        x_train: Union[np.ndarray, scipy.sparse.csr.csr_matrix, pd.DataFrame],
        x_test: Union[np.ndarray, scipy.sparse.csr.csr_matrix, pd.DataFrame],
        y_train: Union[np.ndarray, scipy.sparse.csr.csr_matrix, pd.DataFrame],
        y_test: Union[np.ndarray, scipy.sparse.csr.csr_matrix, pd.DataFrame],
    ) -> Dict[OrderedDict, Any]:
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
            verbose_eval=100,
        )
        return evals_result

    def predict(
        self,
        x_test: Union[np.ndarray, scipy.sparse.csr.csr_matrix],
    ) -> np.ndarray:
        log1p_predictions = self.model.predict(x_test)
        predictions = Expm1Transformer().fit_transform(log1p_predictions)
        return predictions

    def save_as_txt(
        self,
        file_path: str,
    ):
        self.model.save_model(file_path)

    def save_as_onnx(
        self,
        file_path: str,
        sample_input: Union[np.ndarray, scipy.sparse.csr.csr_matrix],
    ):
        initial_types = [["inputs", FloatTensorType([None, sample_input.shape[1]])]]
        onnx_model = onnxmltools.convert_lightgbm(self.model, initial_types=initial_types)
        onnxmltools.utils.save_model(onnx_model, file_path)
