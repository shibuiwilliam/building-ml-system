from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.user import UserCreate, UserModel, UserQuery
from src.repository.base_repository import BaseRepository

logger = getLogger(__name__)


class AbstractUserRepository(ABC, BaseRepository):
    def __init__(self):
        super().__init__()
        pass

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[UserQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[UserModel]:
        raise NotImplementedError

    @abstractmethod
    def select_by_ids(
        self,
        session: Session,
        user_ids: List[str],
        limit=100,
        offset=0,
    ) -> List[UserModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: UserCreate,
        commit: bool = True,
    ) -> Optional[UserModel]:
        raise NotImplementedError
