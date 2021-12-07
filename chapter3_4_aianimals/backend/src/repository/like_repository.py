from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, List, Optional

from sqlalchemy.orm import Session
from src.entities.common import Count
from src.entities.like import LikeCreate, LikeDelete, LikeModel, LikeQuery

logger = getLogger(__name__)


class AbstractLikeRepository(ABC):
    def __init__(self):
        super().__init__()
        pass

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[LikeQuery],
        limit: int = 100,
        offset: int = 0,
    ) -> List[LikeModel]:
        raise NotImplementedError

    @abstractmethod
    def count(
        self,
        session: Session,
        animal_ids: List[str],
    ) -> Dict[str, Count]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: LikeCreate,
        commit: bool = True,
    ) -> Optional[LikeModel]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        session: Session,
        record: LikeDelete,
        commit: bool = True,
    ):
        raise NotImplementedError
