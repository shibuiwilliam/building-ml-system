from abc import ABC, abstractmethod
from logging import getLogger

from sqlalchemy.orm import Session
from src.repository.access_log_repository import AbstractAccessLogRepository
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.access_log import AccessLogCreateRequest

logger = getLogger(__name__)


class AbstractAccessLogUsecase(ABC):
    def __init__(
        self,
        access_log_repository: AbstractAccessLogRepository,
        like_repository: AbstractLikeRepository,
    ):
        self.access_log_repository = access_log_repository
        self.like_repository = like_repository

    @abstractmethod
    def register(
        self,
        session: Session,
        request: AccessLogCreateRequest,
    ):
        raise NotImplementedError
