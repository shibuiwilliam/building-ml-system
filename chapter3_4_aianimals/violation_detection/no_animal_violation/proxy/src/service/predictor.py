from abc import ABC, abstractmethod
from typing import List, Optional

import httpx
import numpy as np
from PIL import Image
from pydantic import BaseModel
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class Prediction(BaseModel):
    violation_probability: float


class AbstractPredictor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _preprocess(
        self,
        img: Image,
    ) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def _predict(self, array: np.ndarray):
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        img: Image,
    ) -> Optional[Prediction]:
        raise NotImplementedError


class NoViolationDetectionPredictor(AbstractPredictor):
    def __init__(
        self,
        url: str = "http://localhost:8501/v1/models/no_animal_violation:predict",
        height: int = 224,
        width: int = 224,
        timeout: float = 10.0,
        retries: int = 3,
    ):
        self.url = url
        self.height = height
        self.width = width
        self.timeout = timeout
        self.transport = httpx.HTTPTransport(
            retries=retries,
        )
        self.headers = {"Content-Type": "application/json"}

    def _preprocess(
        self,
        img: Image,
    ) -> np.ndarray:
        img = img.resize((self.height, self.width))
        array = np.array(img).astype(np.float32) / 255.0
        return array

    def _predict(
        self,
        img_array: np.ndarray,
    ) -> Optional[List]:
        img_list = img_array.tolist()
        request_dict = {"inputs": {"keras_layer_input": [img_list]}}
        with httpx.Client(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            res = client.post(
                self.url,
                data=request_dict,
                headers=self.headers,
            )
        if res.status_code != 200:
            logger.error(f"prediction failed")
            return None
        response = res.json()
        logger.info(f"prediction: {response}")
        return response["outputs"]

    def predict(
        self,
        img: Image,
    ) -> Optional[Prediction]:
        img_array = self._preprocess(img=img)
        prediction = self._predict(img_array=img_array)
        if prediction is None:
            return None
        return Prediction(violation_probability=prediction[1])
