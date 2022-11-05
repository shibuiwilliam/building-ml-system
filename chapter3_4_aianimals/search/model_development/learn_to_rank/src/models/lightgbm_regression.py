import os
import sys
from typing import Dict, List, Optional, Union

import cloudpickle
import numpy as np
import onnxmltools
import pandas as pd
from lightgbm import LGBMRegressor
from onnxmltools.convert.common.data_types import FloatTensorType
from src.middleware.logger import configure_logger
from src.models.base_model import BaseLearnToRankModel

cloudpickle.register_pickle_by_value(sys.modules[__name__])

logger = configure_logger(__name__)

LIGHT_GBM_LEARN_TO_RANK_REGRESSION = {
    "task": "train",
    "boosting": "gbdt",
    "objective": "regression",
    "num_leaves": 10,
    "learning_rate": 0.01,
    "feature_fraction": 0.5,
    "max_depth": -1,
    "num_iterations": 1000000,
    "num_threads": 0,
    "seed": 1234,
}


class LightGBMLearnToRankRegression(BaseLearnToRankModel):
    def __init__(
        self,
        params: Dict = LIGHT_GBM_LEARN_TO_RANK_REGRESSION,
        early_stopping_rounds: int = 10,
        eval_metrics: Union[str, List[str]] = "mse",
        verbose_eval: int = 10,
    ):
        super().__init__()
        self.name: str = "learn_to_rank_regression"
        self.params: Dict = params
        self.early_stopping_rounds = early_stopping_rounds
        self.eval_metrics = eval_metrics
        self.verbose_eval = verbose_eval
        self.model = None
        self.reset_model(params=self.params)

    def reset_model(
        self,
        params: Optional[Dict] = None,
    ):
        if params is not None:
            self.params = params
        logger.info(f"params: {self.params}")
        self.model = LGBMRegressor(**self.params)
        logger.info(f"initialized model: {self.model}")

    def train(
        self,
        x_train: Union[np.ndarray, pd.DataFrame],
        y_train: Union[np.ndarray, pd.DataFrame],
        x_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        y_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        q_train: Optional[List[int]] = None,
        q_test: Optional[List[int]] = None,
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

    def save(
        self,
        file_path: str,
    ) -> str:
        file, ext = os.path.splitext(file_path)
        if ext != ".pkl":
            file_path = f"{file}.pkl"
        logger.info(f"save model: {file_path}")
        with open(file_path, "wb") as f:
            cloudpickle.dump(self.model, f)
        return file_path

    def save_onnx(
        self,
        file_path: str,
        batch_size: int = 20,
        feature_size: int = 1,
    ) -> str:
        file, ext = os.path.splitext(file_path)
        if ext != ".onnx":
            file_path = f"{file}.onnx"
        initial_types = [
            ["inputs", FloatTensorType([batch_size, feature_size])],
        ]
        onnx_model = onnxmltools.convert_lightgbm(
            self.model,
            initial_types=initial_types,
        )
        logger.info(f"save model: {file_path}")
        onnxmltools.utils.save_model(onnx_model, file_path)
        return file_path

    def load(
        self,
        file_path: str,
    ):
        logger.info(f"load model: {file_path}")
        with open(file_path, "rb") as f:
            self.model = cloudpickle.load(f)
