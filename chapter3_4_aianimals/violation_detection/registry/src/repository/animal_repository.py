from abc import ABC, abstractmethod
from typing import Optional

from src.entities.animal import AnimalModel, AnimalUpdate
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractAnimalRepository(ABC):
    def __init__(self, database: AbstractDatabase):
        self.database = database

    @abstractmethod
    def update(
        self,
        record: AnimalUpdate,
        commit: bool = True,
    ) -> Optional[AnimalModel]:
        raise NotImplementedError
