from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Tuple

import cloudpickle
import pandas as pd
from src.infrastructure.predictor_client import AbstractPredictor

logger = getLogger(__name__)


class AbstractLearnToRankPredictService(ABC):
    def __init__(
        self,
        predictor: AbstractPredictor,
    ):
        self.predictor = predictor

    @abstractmethod
    def _preprocess(
        self,
        input: pd.DataFrame,
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def _predict(
        self,
        input: List[List[float]],
    ) -> List[float]:
        raise NotImplementedError

    @abstractmethod
    def _postprocess(
        self,
        input: pd.DataFrame,
        prediction: List[float],
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
        predictor: AbstractPredictor,
        preprocess_file_path: str,
    ):
        super().__init__(predictor=predictor)
        self.preprocess_file_path = preprocess_file_path
        self.__load_preprocess()

    def __load_preprocess(self):
        with open(self.preprocess_file_path, "rb") as f:
            self.preprocess = cloudpickle.load(f)

    def _preprocess(
        self,
        input: pd.DataFrame,
    ) -> pd.DataFrame:
        return self.preprocess.transform(input)

    def _predict(
        self,
        input: List[List[float]],
    ) -> List[float]:
        return self.predictor.predict(input)

    def _postprocess(
        self,
        input: pd.DataFrame,
        prediction: List[float],
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
