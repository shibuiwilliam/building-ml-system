import json
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, List, Optional

import httpx
import numpy as np
from PIL import Image
from pydantic import BaseModel

logger = getLogger(__name__)


class Prediction(BaseModel):
    animal_ids: List[str]
    similarities: List[float]


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


class SimilarImageSearchPredictor(AbstractPredictor):
    def __init__(
        self,
        url: str = "http://localhost:8501/v1/models/similar_image_search:predict",
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
        array = np.array(img).reshape((1, self.height, self.width, 3)).astype(np.float32) / 255.0
        return array

    def _predict(
        self,
        img_array: np.ndarray,
        k: int = 32,
    ) -> Optional[Dict]:
        img_list = img_array.tolist()
        request_dict = {
            "inputs": {
                "k": k,
                "image": img_list,
            },
        }
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
        return Prediction(
            animal_ids=prediction["output_1"][0],
            similarities=prediction["output_0"][0],
        )
