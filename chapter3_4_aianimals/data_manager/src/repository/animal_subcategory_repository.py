from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.animal_subcategory import AnimalSubcategoryCreate, AnimalSubcategoryModel, AnimalSubcategoryQuery
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractAnimalSubcategoryRepository(ABC):
    def __init__(self):
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
