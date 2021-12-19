from abc import ABC, abstractmethod
from logging import getLogger
from typing import Optional

from src.entities.animal import AnimalSearchQuery, AnimalSearchResults
from src.infrastructure.search import AbstractSearch

logger = getLogger(__name__)


class AbstractAnimalSearchRepository(ABC):
    def __init__(
        self,
        search_client: AbstractSearch,
    ):
        self.search_client = search_client
        self.animal_index = "animal"

    @abstractmethod
    def search(
        self,
        query: Optional[AnimalSearchQuery] = None,
        from_: int = 0,
        size: int = 20,
    ) -> AnimalSearchResults:
        raise NotImplementedError
