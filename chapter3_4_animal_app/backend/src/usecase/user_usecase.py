from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.repository.user_repository import AbstractUserRepository
from src.request_object.user import UserCreateRequest, UserRequest
from src.response_object.user import UserResponse

logger = getLogger(__name__)


class AbstractUserUsecase(ABC):
    def __init__(
        self,
        user_repository: AbstractUserRepository,
    ):
        self.user_repository = user_repository

    @abstractmethod
    def retrieve(
        self,
        session: Session,
        request: Optional[UserRequest] = None,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[UserResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        session: Session,
        request: UserCreateRequest,
    ) -> Optional[UserResponse]:
        raise NotImplementedError
