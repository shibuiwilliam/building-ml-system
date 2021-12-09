from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.sql.functions import current_timestamp
from src.schema.base import Base
from src.schema.table import TABLES

logger = getLogger(__name__)


class Like(Base):
    __tablename__ = TABLES.LIKE.value
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
    user_id = Column(
        String(32),
        ForeignKey(f"{TABLES.USER.value}.id"),
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
