from abc import ABC, abstractmethod
from typing import List, Optional

from src.entities.violation import ViolationCreate, ViolationModel, ViolationQuery
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractViolationRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.database = database

    @abstractmethod
    def select(
        self,
        query: Optional[ViolationQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[ViolationModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        record: ViolationCreate,
        commit: bool = True,
    ) -> Optional[ViolationModel]:
        raise NotImplementedError