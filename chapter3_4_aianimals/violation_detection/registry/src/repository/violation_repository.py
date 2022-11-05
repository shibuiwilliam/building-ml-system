import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy import and_
from src.entities.violation import ViolationCreate, ViolationModel, ViolationQuery
from src.infrastructure.database import AbstractDatabase
from src.schema.table import TABLES
from src.schema.violation import Violation


class AbstractViolationRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.logger = logging.getLogger(__name__)
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


class ViolationRepository(AbstractViolationRepository):
    def __init__(
        self,
        database: AbstractDatabase,
    ) -> None:
        super().__init__(database=database)
        self.table_name = TABLES.VIOLATION.value

    def select(
        self,
        query: Optional[ViolationQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[ViolationModel]:
        session = self.database.get_session().__next__()
        try:
            filters = []
            if query is not None:
                if query.id is not None:
                    filters.append(Violation.id == query.id)
                if query.animal_id is not None:
                    filters.append(Violation.animal_id == query.animal_id)
                if query.violation_type_id is not None:
                    filters.append(Violation.violation_type_id == query.violation_type_id)
                if query.probability_lower_bound is not None:
                    filters.append(Violation.probability >= query.probability_lower_bound)
                if query.probability_upper_bound is not None:
                    filters.append(Violation.probability <= query.probability_upper_bound)
                if query.judge is not None:
                    filters.append(Violation.judge == query.judge)
                if query.is_effective is not None:
                    filters.append(Violation.is_effective == query.is_effective)
                if query.is_administrator_checked is not None:
                    filters.append(Violation.is_administrator_checked == query.is_administrator_checked)
            results = session.query(Violation).filter(and_(*filters)).order_by(Violation.id).limit(limit).offset(offset)
            data = [
                ViolationModel(
                    id=d.id,
                    animal_id=d.animal_id,
                    violation_type_id=d.violation_type_id,
                    probability=d.probability,
                    judge=d.judge,
                    is_effective=d.is_effective,
                    is_administrator_checked=d.is_administrator_checked,
                    created_at=d.created_at,
                    updated_at=d.updated_at,
                )
                for d in results
            ]
            return data
        except Exception as e:
            raise e
        finally:
            session.close()

    def insert(
        self,
        record: ViolationCreate,
        commit: bool = True,
    ) -> Optional[ViolationModel]:
        session = self.database.get_session().__next__()
        try:
            data = Violation(**record.dict())
            session.add(data)
            if commit:
                session.commit()
                session.refresh(data)
                result = self.select(
                    query=ViolationQuery(id=data.id),
                    limit=1,
                    offset=0,
                )
                return result[0]
            return None
        except Exception as e:
            raise e
        finally:
            session.close()
