from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql.functions import current_timestamp
from src.middleware.logger import configure_logger
from src.schema.base import Base
from src.schema.table import TABLES

logger = configure_logger(__name__)


class ViolationType(Base):
    __tablename__ = TABLES.VIOLATION_TYPE.value
    id = Column(
        String(32),
        primary_key=True,
    )
    name = Column(
        String(32),
        nullable=False,
        unique=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )