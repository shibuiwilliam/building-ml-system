from abc import ABC, abstractmethod
from typing import List

from src.entities.access_log import AccessLogCreate
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractAccessLogRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.database = database

    @abstractmethod
    def insert(
        self,
        record: AccessLogCreate,
        commit: bool = True,
    ):
        raise NotImplementedError

    @abstractmethod
    def bulk_insert(
        self,
        records: List[AccessLogCreate],
        commit: bool = True,
    ):
        raise NotImplementedError
