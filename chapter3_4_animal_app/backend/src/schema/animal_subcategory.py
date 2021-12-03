from logging import getLogger

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.sql.functions import current_timestamp
from src.schema.base import Base
from src.schema.table import TABLES

logger = getLogger(__name__)


class AnimalSubcategory(Base):
    __tablename__ = TABLES.ANIMAL_SUBCATEGORY.value
    id = Column(
        String(32),
        primary_key=True,
    )
    animal_category_id = Column(
        String(32),
        ForeignKey(f"{TABLES.ANIMAL_CATEGORY.value}.id"),
        nullable=False,
        unique=False,
    )
    name = Column(
        String(128),
        nullable=False,
        unique=False,
    )
    is_deleted = Column(
        Boolean,
        default=False,
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
