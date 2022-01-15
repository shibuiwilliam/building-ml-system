from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.violation import ViolationCreate, ViolationModel, ViolationQuery

logger = getLogger(__name__)


class AbstractViolationRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[ViolationQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[ViolationModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: ViolationCreate,
        commit: bool = True,
    ) -> Optional[ViolationModel]:
        raise NotImplementedError
