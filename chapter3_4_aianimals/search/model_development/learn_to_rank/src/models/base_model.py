import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

import cloudpickle
import numpy as np
import pandas as pd
from src.middleware.logger import configure_logger

cloudpickle.register_pickle_by_value(sys.modules[__name__])

logger = configure_logger(__name__)


class BaseLearnToRankModel(ABC):
    def __init__(self):
        self.name: str = "learn_to_rank"
        self.params: Dict = {}
        self.model = None

    @abstractmethod
    def reset_model(
        self,
        params: Optional[Dict] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def train(
        self,
        x_train: Union[np.ndarray, pd.DataFrame],
        y_train: Union[np.ndarray, pd.DataFrame],
        x_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        y_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        q_train: Optional[List[int]] = None,
        q_test: Optional[List[int]] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        file_path: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def save_onnx(
        self,
        file_path: str,
        batch_size: int = 20,
        feature_size: int = 1,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
        file_path: str,
    ):
        raise NotImplementedError
