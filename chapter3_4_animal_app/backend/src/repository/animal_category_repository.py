from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.animal_category import AnimalCategoryQuery, AnimalCategoryModel, AnimalCategoryCreate
from src.repository.base_repository import BaseRepository
from src.schema.table import TABLES

logger = getLogger(__name__)


class AnimalCategoryRepository(ABC, BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name: str = TABLES.ANIMAL_CATEGORY.value

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[AnimalCategoryQuery],
    ) -> List[AnimalCategoryModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: AnimalCategoryCreate,
        commit: bool = True,
    ) -> Optional[AnimalCategoryModel]:
        raise NotImplementedError
