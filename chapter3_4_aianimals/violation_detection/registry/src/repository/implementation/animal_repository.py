from typing import Optional

from src.entities.animal import AnimalModel, AnimalUpdate
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository

logger = configure_logger(__name__)


class AnimalRepository(AbstractAnimalRepository):
    def __init__(self, database: AbstractDatabase) -> None:
        super().__init__(database=database)

    def update(
        self,
        record: AnimalUpdate,
        commit: bool = True,
    ) -> Optional[AnimalModel]:
        pass
