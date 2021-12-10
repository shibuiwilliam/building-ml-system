from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from src.middleware.logger import configure_logger
from src.usecase.like_usecase import AbstractLikeUsecase

logger = configure_logger(__name__)


class AbstractLikeController(ABC):
    def __init__(
        self,
        like_usecase: AbstractLikeUsecase,
    ):
        self.like_usecase = like_usecase

    @abstractmethod
    def register(
        self,
        session: Session,
        file_path: str,
    ):
        raise NotImplementedError
