from abc import ABC, abstractmethod
from typing import List, Optional

from src.entities.animal import AnimalModel, AnimalQuery
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractAnimalRepository(ABC):
    def __init__(self, database: AbstractDatabase):
        self.database = database

    @abstractmethod
    def select(
        self,
        query: Optional[AnimalQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalModel]:
        raise NotImplementedError
