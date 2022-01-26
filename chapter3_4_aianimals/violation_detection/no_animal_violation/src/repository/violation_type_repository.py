from abc import ABC, abstractmethod
from typing import List, Optional

from src.entities.violation_type import ViolationTypeModel, ViolationTypeQuery
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractViolationTypeRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.database = database

    @abstractmethod
    def select(
        self,
        query: Optional[ViolationTypeQuery],
    ) -> List[ViolationTypeModel]:
        raise NotImplementedError
