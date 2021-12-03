from logging import getLogger

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import Boolean
from src.schema.base import Base
from src.schema.table import TABLES

logger = getLogger(__name__)


class Animal(Base):
    __tablename__ = TABLES.ANIMAL.value
    id = Column(
        String(32),
        primary_key=True,
    )
    name = Column(
        String(128),
        nullable=False,
        unique=False,
    )
    animal_category_id = Column(
        String(32),
        ForeignKey(f"{TABLES.ANIMAL_CATEGORY.value}.id"),
        nullable=False,
        unique=False,
    )
    animal_subcategory_id = Column(
        String(32),
        ForeignKey(f"{TABLES.ANIMAL_SUBCATEGORY.value}.id"),
        nullable=False,
        unique=False,
    )
    user_id = Column(
        String(32),
        ForeignKey(f"{TABLES.USER.value}.id"),
        nullable=False,
        unique=False,
    )
    description = Column(
        Text,
        nullable=False,
        unique=False,
    )
    photo_url = Column(
        Text,
        nullable=False,
        unique=False,
    )
    deactivated = Column(
        Boolean,
        nullable=False,
        unique=False,
        default=False,
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
