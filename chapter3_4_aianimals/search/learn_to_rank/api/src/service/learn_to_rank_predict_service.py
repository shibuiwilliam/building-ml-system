from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Tuple

import cloudpickle
import numpy as np
import pandas as pd

logger = getLogger(__name__)


class AbstractLearnToRankPredictService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _preprocess(
        self,
        input: pd.DataFrame,
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def _predict(
        self,
        input: pd.DataFrame,
    ) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def _postprocess(
        self,
        input: pd.DataFrame,
        prediction: np.ndarray,
    ) -> List[Tuple[str, float]]:
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        input: pd.DataFrame,
    ) -> List[Tuple[str, float]]:
        raise NotImplementedError


class LearnToRankPredictService(AbstractLearnToRankPredictService):
    def __init__(
        self,
        preprocess_file_path: str,
        predictor_file_path: str,
    ):
        super().__init__()
        self.preprocess_file_path = preprocess_file_path
        self.predictor_file_path = predictor_file_path
        self.__load_preprocess()
        self.__load_predictor()

    def __load_preprocess(self):
        with open(self.preprocess_file_path, "rb") as f:
            self.preprocess = cloudpickle.load(f)

    def __load_predictor(self):
        with open(self.predictor_file_path, "rb") as f:
            self.predictor = cloudpickle.load(f)

    def _preprocess(
        self,
        input: pd.DataFrame,
    ) -> pd.DataFrame:
        return self.preprocess.transform(input)

    def _predict(
        self,
        input: pd.DataFrame,
    ) -> np.ndarray:
        return self.predictor.predict(input)

    def _postprocess(
        self,
        input: pd.DataFrame,
        prediction: np.ndarray,
    ) -> List[Tuple[str, float]]:
        id_prediction = {id: prob for id, prob in zip(input.animal_id, prediction)}
        sort_orders = sorted(id_prediction.items(), key=lambda x: x[1], reverse=True)
        return sort_orders

    def predict(
        self,
        input: pd.DataFrame,
    ) -> List[Tuple[str, float]]:
        preprocessed_input = self._preprocess(input=input)
        prediction = self._predict(input=preprocessed_input)
        id_prediction = self._postprocess(input=input, prediction=prediction)
        return id_prediction
