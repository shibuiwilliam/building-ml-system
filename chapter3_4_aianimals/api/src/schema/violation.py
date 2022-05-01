from logging import getLogger

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import FLOAT, Boolean
from src.schema.base import Base
from src.schema.table import TABLES

logger = getLogger(__name__)


class Violation(Base):
    __tablename__ = TABLES.VIOLATION.value
    id = Column(
        String(32),
        primary_key=True,
    )
    animal_id = Column(
        String(32),
        ForeignKey(f"{TABLES.ANIMAL.value}.id"),
        nullable=False,
        unique=False,
    )
    violation_type_id = Column(
        String(32),
        ForeignKey(f"{TABLES.VIOLATION_TYPE.value}.id"),
        nullable=False,
        unique=False,
    )
    judge = Column(
        String(64),
        nullable=False,
        unique=False,
    )
    probability = Column(
        FLOAT,
        nullable=False,
        unique=False,
    )
    is_effective = Column(
        Boolean,
        nullable=False,
        unique=False,
    )
    is_administrator_checked = Column(
        Boolean,
        nullable=False,
        unique=False,
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
