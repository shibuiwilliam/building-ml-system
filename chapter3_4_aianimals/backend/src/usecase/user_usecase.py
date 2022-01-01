from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.middleware.crypt import AbstractCrypt, Crypt
from src.repository.user_repository import AbstractUserRepository
from src.request_object.user import UserCreateRequest, UserLoginRequest, UserRequest
from src.response_object.user import UserLoginResponse, UserResponse

logger = getLogger(__name__)


class AbstractUserUsecase(ABC):
    def __init__(
        self,
        user_repository: AbstractUserRepository,
        crypt: AbstractCrypt,
    ):
        self.user_repository = user_repository
        self.crypt = crypt

    @abstractmethod
    def retrieve(
        self,
        session: Session,
        request: Optional[UserRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[UserResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        session: Session,
        request: UserCreateRequest,
    ) -> Optional[UserResponse]:
        raise NotImplementedError

    @abstractmethod
    def login(
        self,
        session: Session,
        request: UserLoginRequest,
    ) -> Optional[UserLoginResponse]:
        raise NotImplementedError
