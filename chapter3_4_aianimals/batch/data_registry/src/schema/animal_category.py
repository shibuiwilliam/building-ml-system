from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import INT
from src.schema.base import Base
from src.schema.table import TABLES


class AnimalCategory(Base):
    __tablename__ = TABLES.ANIMAL_CATEGORY.value
    id = Column(
        INT,
        primary_key=True,
    )
    name_en = Column(
        String(128),
        nullable=False,
        unique=False,
    )
    name_ja = Column(
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
