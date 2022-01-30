from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.animal import AnimalCreate, AnimalModel, AnimalQuery
from src.entities.user import UserModel

logger = getLogger(__name__)


class AbstractAnimalRepository(ABC):
    def __init__(self):
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
    def liked_by(
        self,
        session: Session,
        animal_id: str,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
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