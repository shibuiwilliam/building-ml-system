from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, List, Optional

from sqlalchemy.orm import Session
from src.middleware.database import Base
from src.schema.abstract_schema import AbstractCreate, AbstractModel, AbstractQuery

logger = getLogger(__name__)


class AbstractRepository(ABC):
    def __init__(self):
        self.table_name: str = ""

    def model_to_dict(row: Base) -> Dict:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        return d

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[AbstractQuery],
    ) -> List[AbstractModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: AbstractCreate,
        commit: bool = True,
    ) -> Optional[AbstractModel]:
        raise NotImplementedError
