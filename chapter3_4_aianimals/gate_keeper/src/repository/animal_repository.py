from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

from src.entities.animal import ANIMAL_MAPPING, ANIMAL_MAPPING_NAME, AnimalDocument, AnimalModel, AnimalQuery
from src.infrastructure.database import AbstractDatabase
from src.infrastructure.queue import AbstractQueue
from src.infrastructure.search import AbstractSearch
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractAnimalRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
        queue: AbstractQueue,
        search: AbstractSearch,
    ):
        self.database = database
        self.queue = queue
        self.search = search

    @abstractmethod
    def select(
        self,
        query: Optional[AnimalQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalModel]:
        raise NotImplementedError

    @abstractmethod
    def dequeue(self) -> Optional[Tuple[int, str, float, bool]]:
        raise NotImplementedError

    @abstractmethod
    def create_index(
        self,
        index: str = ANIMAL_MAPPING_NAME,
        body: Dict = ANIMAL_MAPPING,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_index(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def create_document(
        self,
        id: str,
        document: AnimalDocument,
        index: str = ANIMAL_MAPPING_NAME,
    ):
        raise NotImplementedError
