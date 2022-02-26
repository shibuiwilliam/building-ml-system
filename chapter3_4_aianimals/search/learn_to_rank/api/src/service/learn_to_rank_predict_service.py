from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional, Tuple

import cloudpickle
import numpy as np
import onnxruntime
import pandas as pd

logger = getLogger(__name__)


class AbstractLearnToRankPredictService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _preprocess(
        self,
        input: pd.DataFrame,
    ) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def _predict(
        self,
        input: pd.DataFrame,
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
        preprocess_file_path: str,
        predictor_file_path: str,
        predictor_batch_size: Optional[int] = None,
        predictor_input_name: Optional[str] = None,
        predictor_output_name: Optional[str] = None,
    ):
        super().__init__()
        self.preprocess_file_path = preprocess_file_path
        self.predictor_file_path = predictor_file_path
        self.is_onnx_predictor = False
        self.predictor_batch_size = predictor_batch_size
        self.predictor_input_name = predictor_input_name
        self.predictor_output_name = predictor_output_name

        self.__load_preprocess()
        self.__load_predictor()

    def __load_preprocess(self):
        with open(self.preprocess_file_path, "rb") as f:
            self.preprocess = cloudpickle.load(f)
        logger.info(f"loaded: {self.preprocess_file_path}")

    def __load_predictor(self):
        if self.predictor_file_path.endswith(".pkl"):
            with open(self.predictor_file_path, "rb") as f:
                self.predictor = cloudpickle.load(f)
            self.is_onnx_predictor = False
        elif self.predictor_file_path.endswith(".onnx"):
            self.predictor = onnxruntime.InferenceSession(self.predictor_file_path)
            self.is_onnx_predictor = True
            if (
                self.predictor_batch_size is None
                or self.predictor_input_name is None
                or self.predictor_output_name is None
            ):
                raise ValueError
        else:
            raise ValueError
        logger.info(f"loaded: {self.predictor_file_path}")

    def _preprocess(
        self,
        input: pd.DataFrame,
    ) -> np.ndarray:
        return self.preprocess.transform(input)

    def _predict_sklearn(
        self,
        input: np.ndarray,
    ) -> List[float]:
        return self.predictor.predict(input).tolist()

    def _predict_onnx(
        self,
        input: np.ndarray,
    ) -> List[float]:
        outputs = []
        for i in range(0, input.shape[0], self.predictor_batch_size):
            x = input[i : i + self.predictor_batch_size].astype("float32")
            if len(x) < self.predictor_batch_size:
                _x = np.zeros((self.predictor_batch_size, x.shape[1])).astype("float32")
                for p in range(len(_x)):
                    _x[p] = x[p]
                x = _x
            output = self.predictor.run(
                [self.predictor_output_name],
                {self.predictor_input_name: x},
            )
            outputs.extend(output[0].tolist())
        return outputs[: input.shape[0]]

    def _predict(
        self,
        input: np.ndarray,
    ) -> List[float]:
        if self.is_onnx_predictor:
            return self._predict_onnx(input=input)
        else:
            return self._predict_sklearn(input=input)

    def _postprocess(
        self,
        input: pd.DataFrame,
        prediction: List[float],
    ) -> List[Tuple[str, float]]:
        id_prediction = {id: prob for id, prob in zip(input.animal_id, prediction)}
        logger.info(f"AAAAAAAAAAAAa: {id_prediction}")
        sort_orders = sorted(id_prediction.items(), key=lambda x: x[1], reverse=True)
        return sort_orders

    def predict(
        self,
        input: pd.DataFrame,
    ) -> List[Tuple[str, float]]:
        preprocessed_input = self._preprocess(input=input)
        logger.info(f"DDDDDDDDDDDDDd: {preprocessed_input.shape}")
        prediction = self._predict(input=preprocessed_input)
        id_prediction = self._postprocess(input=input, prediction=prediction)
        return id_prediction
