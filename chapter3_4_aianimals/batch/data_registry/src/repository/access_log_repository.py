import logging
from abc import ABC, abstractmethod
from typing import List

from src.entities.access_log import AccessLogCreate
from src.infrastructure.database import AbstractDatabase
from src.schema.access_log import AccessLog
from src.schema.table import TABLES


class AbstractAccessLogRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.logger = logging.getLogger(__name__)
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


class AccessLogRepository(AbstractAccessLogRepository):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        super().__init__(database=database)
        self.table_name = TABLES.ACCESS_LOG.value

    def insert(
        self,
        record: AccessLogCreate,
        commit: bool = True,
    ):
        session = self.database.get_session().__next__()
        try:
            data = AccessLog(
                id=record.id,
                search_id=record.search_id,
                phrases=record.phrases,
                animal_category_id=record.animal_category_id,
                animal_subcategory_id=record.animal_subcategory_id,
                sort_by=record.sort_by,
                model_name=record.model_name,
                user_id=record.user_id,
                likes=record.likes,
                animal_id=record.animal_id,
                action=record.action,
                created_at=record.created_at,
            )
            session.add(data)
            if commit:
                session.commit()
                session.refresh(data)
        except Exception as e:
            raise e
        finally:
            session.close()

    def bulk_insert(
        self,
        records: List[AccessLogCreate],
        commit: bool = True,
    ):
        session = self.database.get_session().__next__()
        try:
            data = [d.dict() for d in records]
            session.execute(AccessLog.__table__.insert(), data)
            if commit:
                session.commit()
        except Exception as e:
            raise e
        finally:
            session.close()
