import logging
from abc import ABC, abstractmethod
from typing import List

import gensim
from pydantic import BaseModel


class Prediction(BaseModel):
    similar_word: str
    similarity: float


class AbstractSimilarWordPredictor(ABC):
    def __init__(
        self,
        model_path: str,
    ):
        self.logger = logging.getLogger(__name__)
        self.model_path = model_path

    @abstractmethod
    def load_model(self):
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        word: str,
        topn: int = 10,
    ) -> List[Prediction]:
        raise NotImplementedError


class SimilarWordPredictor(AbstractSimilarWordPredictor):
    def __init__(
        self,
        model_path: str,
    ):
        super().__init__(model_path=model_path)
        self.load_model()

    def load_model(self):
        self.logger.info(f"loading {self.model}")
        self.model = gensim.models.KeyedVectors.load_word2vec_format(
            self.model_path,
            binary=False,
        )
        self.logger.info(f"loaded {self.model}")

    def predict(
        self,
        word: str,
        topn: int = 10,
    ) -> List[Prediction]:
        try:
            similar_words = self.model.most_similar(
                positive=[word],
                topn=topn,
            )
            results = [Prediction(similar_word=w[0], similarity=w[1]) for w in similar_words]
            self.logger.info(f"{word}: {results}")
            return results
        except Exception as e:
            self.logger.error(e)
            return []
