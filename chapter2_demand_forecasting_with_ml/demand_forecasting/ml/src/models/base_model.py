from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Union, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


class SUGGEST_TYPE(Enum):
    CATEGORICAL = "categorical"
    INT = "int"
    UNIFORM = "uniform"


class SearchParams(BaseModel):
    name: str
    suggest_type: SUGGEST_TYPE
    value_range: Any


class BaseDemandForecastingModel(ABC):
    def __init__(self):
        self.name: str = "base_demand_forecasting"
        self.params: Dict = {}
        self.model = None
        self.search_params: List[SearchParams] = []

    @abstractmethod
    def define_default_search_params(self):
        raise NotImplementedError

    @abstractmethod
    def define_search_params(
        self,
        search_params: List[SearchParams],
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
        x_test: Union[np.ndarray, pd.DataFrame],
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
