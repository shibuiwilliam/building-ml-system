from abc import ABC, abstractmethod
from logging import getLogger

from sqlalchemy.orm import Session
from src.entities.access_log import AccessLogCreate

logger = getLogger(__name__)


class AbstractAccessLogRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: AccessLogCreate,
        commit: bool = True,
    ):
        raise NotImplementedError
