from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional, Tuple

import cloudpickle
import numpy as np
import onnxruntime

logger = getLogger(__name__)


class AbstractLearnToRankPredictService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _load_preprocess(self):
        raise NotImplementedError

    @abstractmethod
    def _load_predictor(self):
        raise NotImplementedError

    @abstractmethod
    def transform_likes_scaler(
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
    def _postprocess(
        self,
        ids: List[str],
        prediction: List[float],
    ) -> List[Tuple[str, float]]:
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        ids: List[str],
        input: np.ndarray,
    ) -> List[Tuple[str, float]]:
        raise NotImplementedError


class LearnToRankPredictService(AbstractLearnToRankPredictService):
    def __init__(
        self,
        preprocess_likes_scaler_file_path: str,
        preprocess_query_animal_category_id_encoder_file_path: str,
        preprocess_query_animal_subcategory_id_encoder_file_path: str,
        preprocess_query_phrase_encoder_file_path: str,
        predictor_file_path: str,
        predictor_batch_size: Optional[int] = None,
        predictor_input_name: Optional[str] = None,
        predictor_output_name: Optional[str] = None,
    ):
        super().__init__()
        self.preprocess_likes_scaler_file_path = preprocess_likes_scaler_file_path
        self.preprocess_query_animal_category_id_encoder_file_path = (
            preprocess_query_animal_category_id_encoder_file_path
        )
        self.preprocess_query_animal_subcategory_id_encoder_file_path = (
            preprocess_query_animal_subcategory_id_encoder_file_path
        )
        self.preprocess_query_phrase_encoder_file_path = preprocess_query_phrase_encoder_file_path
        self.predictor_file_path = predictor_file_path

        self.is_onnx_predictor = False
        self.predictor_batch_size = predictor_batch_size
        self.predictor_input_name = predictor_input_name
        self.predictor_output_name = predictor_output_name

        self._load_preprocess()
        self._load_predictor()

    def __load_cloud_pickle(
        self,
        file_path: str,
    ):
        with open(file_path, "rb") as f:
            p = cloudpickle.load(f)
        logger.info(f"loaded: {file_path}")
        return p

    def _load_preprocess(self):
        self.preprocess_likes_scaler = self.__load_cloud_pickle(file_path=self.preprocess_likes_scaler_file_path)
        self.preprocess_query_animal_category_id_encoder = self.__load_cloud_pickle(
            file_path=self.preprocess_query_animal_category_id_encoder_file_path
        )
        self.preprocess_query_animal_subcategory_id_encoder = self.__load_cloud_pickle(
            file_path=self.preprocess_query_animal_subcategory_id_encoder_file_path
        )
        self.preprocess_query_phrase_encoder = self.__load_cloud_pickle(
            file_path=self.preprocess_query_phrase_encoder_file_path
        )

    def _load_predictor(self):
        if self.predictor_file_path.endswith(".pkl"):
            self.predictor = self.__load_cloud_pickle(file_path=self.predictor_file_path)
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

    def transform_likes_scaler(
        self,
        likes: List[List[int]],
    ) -> List[List[float]]:
        return self.preprocess_likes_scaler.transform(likes).tolist()

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
        ids: List[str],
        prediction: List[float],
    ) -> List[Tuple[str, float]]:
        id_prediction = {id: prob for id, prob in zip(ids, prediction)}
        sort_orders = sorted(id_prediction.items(), key=lambda x: x[1], reverse=True)
        return sort_orders

    def predict(
        self,
        ids: List[str],
        input: np.ndarray,
    ) -> List[Tuple[str, float]]:
        prediction = self._predict(input=input)
        id_prediction = self._postprocess(
            ids=ids,
            prediction=prediction,
        )
        logger.info(f"sorted prediction: {id_prediction}")
        return id_prediction
