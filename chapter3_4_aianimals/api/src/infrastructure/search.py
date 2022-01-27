from abc import ABC, abstractmethod
from logging import getLogger
from typing import Optional

from src.entities.animal import AnimalSearchQuery, AnimalSearchResults

logger = getLogger(__name__)


class AbstractSearch(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def search(
        self,
        index: str,
        query: AnimalSearchQuery,
        from_: int = 0,
        size: int = 20,
    ) -> AnimalSearchResults:
        raise NotImplementedError
