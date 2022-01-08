from abc import ABC, abstractmethod
from typing import List, Optional

from src.entities.user import UserCreate, UserModel, UserQuery
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractUserRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.database = database

    @abstractmethod
    def select(
        self,
        query: Optional[UserQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[UserModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        record: UserCreate,
        commit: bool = True,
    ) -> Optional[UserModel]:
        raise NotImplementedError
