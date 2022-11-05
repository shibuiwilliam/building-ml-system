from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import INT
from src.schema.base import Base
from src.schema.table import TABLES


class User(Base):
    __tablename__ = TABLES.USER.value
    id = Column(
        String(32),
        primary_key=True,
    )
    handle_name = Column(
        String(128),
        nullable=False,
        unique=True,
    )
    email_address = Column(
        String(128),
        nullable=False,
        unique=True,
    )
    password = Column(
        String(128),
        nullable=False,
        unique=False,
    )
    age = Column(
        INT,
        nullable=False,
        unique=False,
    )
    gender = Column(
        INT,
        nullable=False,
        unique=False,
    )
    deactivated = Column(
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
