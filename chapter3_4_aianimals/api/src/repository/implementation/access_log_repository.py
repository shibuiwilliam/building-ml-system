from logging import getLogger

from sqlalchemy.orm import Session
from src.entities.access_log import AccessLogCreate
from src.repository.access_log_repository import AbstractAccessLogRepository
from src.schema.access_log import AccessLog
from src.schema.table import TABLES

logger = getLogger(__name__)


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
            phrases=record.phrases,
            animal_category_id=record.animal_category_id,
            animal_subcategory_id=record.animal_subcategory_id,
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
