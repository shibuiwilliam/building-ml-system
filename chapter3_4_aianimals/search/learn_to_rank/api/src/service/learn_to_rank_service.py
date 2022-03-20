from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional, Tuple, Union

import numpy as np
from lightgbm import LGBMRanker, LGBMRegressor
from onnxruntime import InferenceSession
from sklearn.base import BaseEstimator

logger = getLogger(__name__)


class AbstractLearnToRankService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def transform_like_scaler(
        self,
        likes: List[List[int]],
    ) -> List[List[float]]:
        raise NotImplementedError

    @abstractmethod
    def transform_query_animal_category_id_encoder(
        self,
        query_animal_category_id: List[List[Optional[int]]],
    ) -> List[List[float]]:
        raise NotImplementedError

    @abstractmethod
    def transform_query_animal_subcategory_id_encoder(
        self,
        query_animal_subcategory_id: List[List[Optional[int]]],
    ) -> List[List[float]]:
        raise NotImplementedError

    @abstractmethod
    def transform_query_phrase_encoder(
        self,
        query_phrase: List[List[str]],
    ) -> List[List[float]]:
        raise NotImplementedError

    @abstractmethod
    def postprocess(
        self,
        ids: List[str],
        prediction: List[float],
    ) -> List[Tuple[str, float]]:
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        ids: List[str],
        input: List[List[float]],
    ) -> List[Tuple[str, float]]:
        raise NotImplementedError


class LearnToRankService(AbstractLearnToRankService):
    def __init__(
        self,
        preprocess_likes_scaler: BaseEstimator,
        preprocess_query_animal_category_id_encoder: BaseEstimator,
        preprocess_query_animal_subcategory_id_encoder: BaseEstimator,
        preprocess_query_phrase_encoder: BaseEstimator,
        predictor: Union[BaseEstimator, LGBMRanker, LGBMRegressor, InferenceSession],
        is_onnx_predictor: bool = False,
        predictor_batch_size: Optional[int] = None,
        predictor_input_name: Optional[str] = None,
        predictor_output_name: Optional[str] = None,
    ):
        super().__init__()

        self.preprocess_like_scaler = preprocess_likes_scaler
        self.preprocess_query_animal_category_id_encoder = preprocess_query_animal_category_id_encoder
        self.preprocess_query_animal_subcategory_id_encoder = preprocess_query_animal_subcategory_id_encoder
        self.preprocess_query_phrase_encoder = preprocess_query_phrase_encoder
        self.predictor = predictor
        self.is_onnx_predictor = is_onnx_predictor
        self.predictor_batch_size = predictor_batch_size
        self.predictor_input_name = predictor_input_name
        self.predictor_output_name = predictor_output_name

    def transform_like_scaler(
        self,
        likes: List[List[int]],
    ) -> List[List[float]]:
        return self.preprocess_like_scaler.transform(likes).tolist()

    def transform_query_animal_category_id_encoder(
        self,
        query_animal_category_id: List[List[Optional[int]]],
    ) -> List[List[float]]:
        return self.preprocess_query_animal_category_id_encoder.transform(query_animal_category_id).toarray().tolist()

    def transform_query_animal_subcategory_id_encoder(
        self,
        query_animal_subcategory_id: List[List[Optional[int]]],
    ) -> List[List[float]]:
        return (
            self.preprocess_query_animal_subcategory_id_encoder.transform(query_animal_subcategory_id)
            .toarray()
            .tolist()
        )

    def transform_query_phrase_encoder(
        self,
        query_phrase: List[List[str]],
    ) -> List[List[float]]:
        return self.preprocess_query_phrase_encoder.transform(query_phrase).toarray().tolist()

    def _predict_sklearn(
        self,
        input: List[List[float]],
    ) -> List[float]:
        return self.predictor.predict(input).tolist()

    def _predict_onnx(
        self,
        input: List[List[float]],
    ) -> List[float]:
        if self.predictor_batch_size is None:
            raise ValueError

        outputs = []
        _input = np.array(input)
        for i in range(0, _input.shape[0], self.predictor_batch_size):
            x = _input[i : i + self.predictor_batch_size].astype("float32")
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
        return outputs[: _input.shape[0]]

    def _predict(
        self,
        input: List[List[float]],
    ) -> List[float]:
        if self.is_onnx_predictor:
            return self._predict_onnx(input=input)
        else:
            return self._predict_sklearn(input=input)

    def postprocess(
        self,
        ids: List[str],
        prediction: List[float],
    ) -> List[Tuple[str, float]]:
        id_prediction = {id: prob for id, prob in zip(ids, prediction)}
        sort_orders = sorted(id_prediction.items(), key=lambda x: x[1], reverse=True)
        return sort_orders

    def predict(
        self,
        ids: List[str],
        input: List[List[float]],
    ) -> List[Tuple[str, float]]:
        prediction = self._predict(input=input)
        id_prediction = self.postprocess(
            ids=ids,
            prediction=prediction,
        )
        logger.info(f"sorted prediction: {id_prediction}")
        return id_prediction
