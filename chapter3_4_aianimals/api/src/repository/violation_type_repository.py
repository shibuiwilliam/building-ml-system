from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.entities.violation_type import ViolationTypeCreate, ViolationTypeModel, ViolationTypeQuery
from src.schema.table import TABLES
from src.schema.violation_type import ViolationType

logger = getLogger(__name__)


class AbstractViolationTypeRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[ViolationTypeQuery] = None,
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


class ViolationTypeRepository(AbstractViolationTypeRepository):
    def __init__(self):
        super().__init__()
        self.table_name = TABLES.VIOLATION_TYPE.value

    def select(
        self,
        session: Session,
        query: Optional[ViolationTypeQuery] = None,
    ) -> List[ViolationTypeModel]:
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(ViolationType.id == query.id)
            if query.name is not None:
                filters.append(ViolationType.name == query.name)
        results = session.query(ViolationType).filter(and_(*filters)).order_by(ViolationType.id).all()
        data = [
            ViolationTypeModel(
                id=d.id,
                name=d.name,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in results
        ]
        return data

    def insert(
        self,
        session: Session,
        record: ViolationTypeCreate,
        commit: bool = True,
    ) -> Optional[ViolationTypeModel]:
        data = ViolationType(**record.dict())
        session.add(data)
        if commit:
            session.commit()
            session.refresh(data)
            result = self.select(
                session=session,
                query=ViolationTypeQuery(id=data.id),
            )
            return result[0]
        return None
