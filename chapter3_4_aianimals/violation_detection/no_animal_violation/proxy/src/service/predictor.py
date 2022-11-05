import json
import logging
from abc import ABC, abstractmethod
from typing import List, Optional

import httpx
import numpy as np
from PIL import Image
from pydantic import BaseModel


class Prediction(BaseModel):
    violation_probability: float


class AbstractPredictor(ABC):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

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
        super().__init__()
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
        array = np.array(img).reshape((1, self.height, self.width, 3)).astype(np.float32) / 255.0
        return array

    def _predict(
        self,
        img_array: np.ndarray,
    ) -> Optional[List]:
        img_list = img_array.tolist()
        request_dict = {"inputs": {"keras_layer_input": img_list}}
        with httpx.Client(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            res = client.post(
                self.url,
                data=json.dumps(request_dict),
                headers=self.headers,
            )
        if res.status_code != 200:
            self.logger.error(f"prediction failed")
            return None
        response = res.json()
        self.logger.info(f"prediction: {response}")
        return response["outputs"][0]

    def predict(
        self,
        img: Image,
    ) -> Optional[Prediction]:
        img_array = self._preprocess(img=img)
        prediction = self._predict(img_array=img_array)
        if prediction is None:
            return None
        return Prediction(violation_probability=prediction[1])
