from abc import ABC, abstractmethod
from typing import List, Optional

from src.entities.animal_category import AnimalCategoryCreate, AnimalCategoryModel, AnimalCategoryQuery
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractAnimalCategoryRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.database = database

    @abstractmethod
    def select(
        self,
        query: Optional[AnimalCategoryQuery],
    ) -> List[AnimalCategoryModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        record: AnimalCategoryCreate,
        commit: bool = True,
    ) -> Optional[AnimalCategoryModel]:
        raise NotImplementedError
