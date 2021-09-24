from abc import ABC, abstractmethod
from typing import Union

import numpy as np
import pandas as pd
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


class BaseDemandForecastingModel(ABC):
    def __init__(self):
        self.params = None
        self.model = None

    @abstractmethod
    def train(
        self,
        x_train: Union[np.ndarray, pd.DataFrame],
        x_test: Union[np.ndarray, pd.DataFrame],
        y_train: Union[np.ndarray, pd.DataFrame],
        y_test: Union[np.ndarray, pd.DataFrame],
    ):
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        x_test: Union[np.ndarray, pd.DataFrame],
    ) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        file_path: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def load(
        self,
        file_path: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def save_as_onnx(
        self,
        file_path: str,
        sample_input: Union[np.ndarray, pd.DataFrame],
    ):
        raise NotImplementedError
