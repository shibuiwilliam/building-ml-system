from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class BaseDemandForecastingModel(ABC):
    def __init__(self):
        self.name: str = "base_beverage_sales_forecasting"
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
    ):
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        x: Union[np.ndarray, pd.DataFrame],
    ) -> Union[np.ndarray, pd.DataFrame]:
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
