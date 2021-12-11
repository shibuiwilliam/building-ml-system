from abc import ABC, abstractmethod
from typing import Dict

from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository

logger = configure_logger(__name__)


class AbstractAnimalUsecase(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
    ):
        self.animal_repository = animal_repository

    @abstractmethod
    def create_index(self):
        raise NotImplementedError

    @abstractmethod
    def get_index(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def index_exists(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def register_index(self):
        raise NotImplementedError
