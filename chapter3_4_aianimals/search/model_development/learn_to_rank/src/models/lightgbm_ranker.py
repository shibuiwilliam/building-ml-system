import os
from typing import Dict, List, Optional, Union

import cloudpickle
import numpy as np
import pandas as pd
from lightgbm import LGBMRanker
from src.middleware.logger import configure_logger
from src.models.base_model import BaseLearnToRankModel

logger = configure_logger(__name__)

LIGHT_GBM_LEARN_TO_RANK_RANKER = {
    "task": "train",
    "objective": "lambdarank",
    "metric": "ndcg",
    "lambdarank_truncation_level": 10,
    "ndcg_eval_at": [10, 5, 20],
    "n_estimators": 10000,
    "boosting_type": "gbdt",
    "num_leaves": 50,
    "learning_rate": 0.1,
    "max_depth": -1,
    "num_iterations": 10000,
    "num_threads": 0,
    "seed": 1234,
}


class LightGBMLearnToRankRanker(BaseLearnToRankModel):
    def __init__(
        self,
        params: Dict = LIGHT_GBM_LEARN_TO_RANK_RANKER,
        early_stopping_rounds: int = 5,
        eval_metrics: Union[str, List[str]] = "mse",
        verbose_eval: int = 1,
    ):
        super().__init__()
        self.name: str = "learn_to_rank_ranker"
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
        self.model = LGBMRanker(**self.params)
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
            group=q_train,
            eval_set=eval_set,
            early_stopping_rounds=self.early_stopping_rounds,
            eval_group=[q_train, q_test],
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
        logger.info("pass")
        return ""

    def load(
        self,
        file_path: str,
    ):
        logger.info(f"load model: {file_path}")
        with open(file_path, "rb") as f:
            self.model = cloudpickle.load(f)
