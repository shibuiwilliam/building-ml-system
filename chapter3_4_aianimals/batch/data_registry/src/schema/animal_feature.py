from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql.functions import current_timestamp
from src.middleware.logger import configure_logger
from src.schema.base import Base
from src.schema.table import TABLES

logger = configure_logger(__name__)


class AnimalFeature(Base):
    __tablename__ = TABLES.ANIMAL_FEATURE.value
    id = Column(
        String(32),
        ForeignKey(f"{TABLES.ANIMAL.value}.id"),
        primary_key=True,
    )
    name_words = Column(
        JSON,
        nullable=True,
        unique=False,
    )
    name_vector = Column(
        JSON,
        nullable=True,
        unique=False,
    )
    description_words = Column(
        JSON,
        nullable=True,
        unique=False,
    )
    description_vector = Column(
        JSON,
        nullable=True,
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
