from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.like import LikeDelete, LikeModel, LikeQuery
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractLikeRepository(ABC):
    def __init__(self):
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
    def delete(
        self,
        session: Session,
        record: LikeDelete,
        commit: bool = True,
    ):
        raise NotImplementedError
