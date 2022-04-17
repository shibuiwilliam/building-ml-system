from abc import ABC, abstractmethod
from logging import getLogger

from sqlalchemy.orm import Session
from src.entities.access_log import AccessLogCreate
from src.schema.access_log import AccessLog
from src.schema.table import TABLES

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


class AccessLogRepository(AbstractAccessLogRepository):
    def __init__(self):
        super().__init__()
        self.table_name = TABLES.ACCESS_LOG.value

    def insert(
        self,
        session: Session,
        record: AccessLogCreate,
        commit: bool = True,
    ):
        action = record.action.value
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
            action=action,
            created_at=record.created_at,
        )
        session.add(data)
        if commit:
            session.commit()
            session.refresh(data)
