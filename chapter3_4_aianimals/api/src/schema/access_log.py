from logging import getLogger

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import INT
from src.schema.base import Base
from src.schema.table import TABLES

logger = getLogger(__name__)


class AccessLog(Base):
    __tablename__ = TABLES.ACCESS_LOG.value
    id = Column(
        String(32),
        primary_key=True,
    )
    search_id = Column(
        String(64),
        nullable=False,
        unique=False,
    )
    phrases = Column(
        JSON,
        nullable=False,
        unique=False,
    )
    animal_category_id = Column(
        INT,
        ForeignKey(f"{TABLES.ANIMAL_CATEGORY.value}.id"),
        nullable=True,
        unique=False,
    )
    animal_subcategory_id = Column(
        INT,
        ForeignKey(f"{TABLES.ANIMAL_SUBCATEGORY.value}.id"),
        nullable=True,
        unique=False,
    )
    sort_by = Column(
        String(64),
        nullable=False,
        unique=False,
    )
    model_name = Column(
        String(64),
        nullable=True,
        unique=False,
    )
    user_id = Column(
        String(32),
        ForeignKey(f"{TABLES.USER.value}.id"),
        nullable=False,
        unique=False,
    )
    likes = Column(
        INT,
        nullable=False,
        unique=False,
    )
    animal_id = Column(
        String(32),
        ForeignKey(f"{TABLES.ANIMAL.value}.id"),
        nullable=False,
        unique=False,
    )
    action = Column(
        String(32),
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
