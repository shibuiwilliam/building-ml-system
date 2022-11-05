import logging
from abc import ABC, abstractmethod

from src.configurations import Configurations
from src.usecase.similar_word_usecase import AbstractSimilarWordUsecase


class AbstractSimilarWordRegistrationJob(ABC):
    def __init__(
        self,
        similar_word_usecase: AbstractSimilarWordUsecase,
    ):
        self.logger = logging.getLogger(__name__)
        self.similar_word_usecase = similar_word_usecase

    @abstractmethod
    def run(self):
        raise NotImplementedError


class SimilarWordRegistrationJob(AbstractSimilarWordRegistrationJob):
    def __init__(
        self,
        similar_word_usecase: AbstractSimilarWordUsecase,
    ):
        super().__init__(similar_word_usecase=similar_word_usecase)

    def run(self):
        self.similar_word_usecase.register(top_n=Configurations.search_top_n)
