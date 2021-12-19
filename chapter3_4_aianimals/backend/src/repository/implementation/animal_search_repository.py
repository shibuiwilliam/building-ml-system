from logging import getLogger
from typing import Optional

from src.entities.animal import AnimalSearchQuery, AnimalSearchResults
from src.infrastructure.search import AbstractSearch
from src.repository.animal_search_repository import AbstractAnimalSearchRepository

logger = getLogger(__name__)


class AnimalSearchRepository(AbstractAnimalSearchRepository):
    def __init__(
        self,
        search_client: AbstractSearch,
    ):
        super().__init__(search_client=search_client)

    def search(
        self,
        query: Optional[AnimalSearchQuery] = None,
        from_: int = 0,
        size: int = 20,
    ) -> AnimalSearchResults:
        results = self.search_client.search(
            index=self.animal_index,
            query=query,
            from_=from_,
            size=size,
        )
        return results
