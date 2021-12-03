from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.animal_subcategory import AnimalSubcategoryCreate, AnimalSubcategoryModel, AnimalSubcategoryQuery
from src.repository.base_repository import BaseRepository

logger = getLogger(__name__)


class AbstractAnimalSubcategoryRepository(ABC, BaseRepository):
    def __init__(self):
        super().__init__()
        pass

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
