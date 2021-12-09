from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from src.middleware.logger import configure_logger
from src.usecase.user_usecase import AbstractUserUsecase

logger = configure_logger(__name__)


class AbstractUserController(ABC):
    def __init__(
        self,
        user_usecase: AbstractUserUsecase,
    ):
        self.user_usecase = user_usecase

    @abstractmethod
    def register(
        self,
        session: Session,
        file_path: str,
    ):
        raise NotImplementedError
