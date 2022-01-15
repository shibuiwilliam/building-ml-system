from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.user import UserCreate, UserLoginAssertion, UserLoginQuery, UserModel, UserQuery

logger = getLogger(__name__)


class AbstractUserRepository(ABC):
    def __init__(self):
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

    @abstractmethod
    def assert_login(
        self,
        session: Session,
        login_query: UserLoginQuery,
    ) -> Optional[UserLoginAssertion]:
        raise NotImplementedError
