from abc import ABC, abstractmethod

from src.middleware.logger import configure_logger
from src.usecase.animal_usecase import AbstractAnimalUsecase

logger = configure_logger(__name__)


class AbstractAnimalController(ABC):
    def __init__(
        self,
        animal_usecase: AbstractAnimalUsecase,
    ):
        self.animal_usecase = animal_usecase

    @abstractmethod
    def run(self):
        raise NotImplementedError
