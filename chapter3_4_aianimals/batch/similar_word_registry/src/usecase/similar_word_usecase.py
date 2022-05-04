import logging
from abc import ABC, abstractmethod
from typing import Dict, List

from src.configurations import Configurations
from src.constants import CONSTANTS
from src.infrastructure.cache import AbstractCache
from src.repository.access_log_repository import AbstractAccessLogRepository
from src.service.similar_word_predictor import AbstractSimilarWordPredictor, Prediction


class AbstractSimilarWordUsecase(ABC):
    def __init__(
        self,
        access_log_repository: AbstractAccessLogRepository,
        cache_client: AbstractCache,
        similar_word_predictor: AbstractSimilarWordPredictor,
    ):
        self.logger = logging.getLogger(__name__)
        self.access_log_repository = access_log_repository
        self.cache_client = cache_client
        self.similar_word_predictor = similar_word_predictor

    @abstractmethod
    def register(
        self,
        top_n: int = 100,
    ):
        raise NotImplementedError


class SimilarWordUsecase(AbstractSimilarWordUsecase):
    def __init__(
        self,
        access_log_repository: AbstractAccessLogRepository,
        cache_client: AbstractCache,
        similar_word_predictor: AbstractSimilarWordPredictor,
    ):
        super().__init__(
            access_log_repository=access_log_repository,
            cache_client=cache_client,
            similar_word_predictor=similar_word_predictor,
        )

    def __make_cache_key(
        self,
        word: str,
    ) -> str:
        return f"SIMILAR_WORD_{word}"

    def __make_cache_value(
        self,
        similar_words: List[Prediction],
    ) -> str:
        value_list = [f"{p.similar_word}{CONSTANTS.SPLITTER}{p.similarity}" for p in similar_words]
        value = f"{CONSTANTS.SPLITTER}{CONSTANTS.SPLITTER}".join(value_list)
        return value

    def register(
        self,
        top_n: int = 100,
    ):
        self.logger.info("start")
        data: Dict[str, int] = {}
        limit = 200
        offset = 0
        while True:
            access_logs = self.access_log_repository.select(
                limit=limit,
                offset=offset,
            )
            if len(access_logs) == 0:
                break
            for access_log in access_logs:
                for a in access_log.phrases:
                    if a in data.keys():
                        data[a] += 1
                    else:
                        data[a] = 1
            offset += limit
        sorted_data = sorted(
            data.items(),
            key=lambda item: item[1],
            reverse=True,
        )
        top_words: Dict[str, float] = {k: v for k, v in sorted_data[:top_n]}
        self.logger.info(f"top {top_n} search keys: {top_words}")
        num = 0
        for word in top_words.keys():
            similar_words = self.similar_word_predictor.predict(
                word=word,
                topn=Configurations.similar_top_n,
            )
            cache_key = self.__make_cache_key(word=word)
            cache_value = self.__make_cache_value(similar_words=similar_words)
            self.cache_client.set(
                key=cache_key,
                value=cache_value,
            )
            num += len(similar_words)
        self.logger.info(f"DONE registered {num} similar words")
