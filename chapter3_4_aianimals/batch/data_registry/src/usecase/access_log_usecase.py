from abc import ABC, abstractmethod
from typing import List

from src.middleware.logger import configure_logger
from src.repository.access_log_repository import AbstractAccessLogRepository
from src.request_object.access_log import AccessLogCreateRequest

logger = configure_logger(__name__)


class AbstractAccessLogUsecase(ABC):
    def __init__(
        self,
        access_log_repository: AbstractAccessLogRepository,
    ):
        self.access_log_repository = access_log_repository

    @abstractmethod
    def register(
        self,
        request: AccessLogCreateRequest,
    ):
        raise NotImplementedError

    @abstractmethod
    def bulk_register(
        self,
        requests: List[AccessLogCreateRequest],
    ):
        raise NotImplementedError
