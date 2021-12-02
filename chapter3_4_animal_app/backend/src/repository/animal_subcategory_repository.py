from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.animal_subcategory import AnimalSubcategoryModel, AnimalSubcategoryCreate, AnimalSubcategoryQuery
from src.repository.base_repository import BaseRepository
from src.schema.table import TABLES

logger = getLogger(__name__)


class AnimalSubcategoryRepository(ABC, BaseRepository):
    def __init__(self):
        super().__init__()
        self.table_name: str = TABLES.ANIMAL_SUBCATEGORY.value

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[AnimalSubcategoryQuery],
    ) -> List[AnimalSubcategoryModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: AnimalSubcategoryCreate,
        commit: bool = True,
    ) -> Optional[AnimalSubcategoryModel]:
        raise NotImplementedError
