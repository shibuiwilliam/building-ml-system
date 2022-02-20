from abc import ABC, abstractmethod
from logging import getLogger
from typing import List

import httpx

logger = getLogger(__name__)


class AbstractPredictor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def predict(
        self,
        input: List[List[float]],
    ) -> List[float]:
        raise NotImplementedError


class Predictor(AbstractPredictor):
    def __init__(
        self,
        endpoint: str,
        input_name: str,
        output_name: str,
        batch_size: int = 32,
        feature_size: int = 200,
        retries: int = 3,
        timeout: int = 2,
    ):
        self.endpoint = endpoint
        self.input_name = input_name
        self.output_name = output_name
        self.batch_size = batch_size
        self.feature_size = feature_size
        self.zero_feature = [0.0 for _ in range(self.feature_size)]
        self.retries = retries
        self.timeout = timeout
        self.transport = httpx.HTTPTransport(
            retries=self.retries,
        )
        self.headers = {"Content-Type": "application/json"}

    def predict(
        self,
        input: List[List[float]],
    ) -> List[float]:
        predictions = []
        for i in range(0, len(input), self.batch_size):
            x = input[i : i + self.batch_size]
            if len(x) < self.batch_size:
                x.extend([self.zero_feature for _ in range(self.batch_size - len(x))])
            data = {self.input_name: x}
            with httpx.Client(
                timeout=self.timeout,
                transport=self.transport,
            ) as client:
                response = client.post(
                    url=self.endpoint,
                    headers=self.headers,
                    data=data,
                )
            if response.status_code != 200:
                logger.error(f"failed prediction: {response.status_code}")
                return []
            r = response.json()
            prediction = r[self.output_name]
            prediction = prediction[: self.batch_size - len(x)]
            predictions.extend(prediction)
        return predictions
