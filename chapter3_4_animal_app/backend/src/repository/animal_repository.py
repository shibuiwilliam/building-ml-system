from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.animal import AnimalCreate, AnimalModel, AnimalModelWithLike, AnimalQuery
from src.entities.user import UserModel
from src.repository.base_repository import BaseRepository

logger = getLogger(__name__)


class AbstractAnimalRepository(ABC, BaseRepository):
    def __init__(self):
        super().__init__()
        pass

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[AnimalQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalModel]:
        raise NotImplementedError

    @abstractmethod
    def select_with_like(
        self,
        session: Session,
        query: Optional[AnimalQuery],
        order_by_like: bool = True,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalModelWithLike]:
        raise NotImplementedError

    @abstractmethod
    def liked_by(
        self,
        session: Session,
        animal_id: str,
    ) -> List[UserModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: AnimalCreate,
        commit: bool = True,
    ) -> Optional[AnimalModel]:
        raise NotImplementedError
