from abc import ABC, abstractmethod
from typing import List, Optional

from src.entities.like import LikeCreate, LikeModel, LikeQuery
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractLikeRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.database = database

    @abstractmethod
    def select(
        self,
        query: Optional[LikeQuery],
        limit: int = 100,
        offset: int = 0,
    ) -> List[LikeModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        record: LikeCreate,
        commit: bool = True,
    ) -> Optional[LikeModel]:
        raise NotImplementedError
