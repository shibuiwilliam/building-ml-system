from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.violation_type import ViolationTypeCreate, ViolationTypeModel, ViolationTypeQuery

logger = getLogger(__name__)


class AbstractViolationTypeRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[ViolationTypeQuery],
    ) -> List[ViolationTypeModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: ViolationTypeCreate,
        commit: bool = True,
    ) -> Optional[ViolationTypeModel]:
        raise NotImplementedError
