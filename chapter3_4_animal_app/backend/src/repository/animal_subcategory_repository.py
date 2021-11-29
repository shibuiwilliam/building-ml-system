from logging import getLogger
from typing import List, Optional, Tuple

from pydantic import BaseModel
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import FLOAT, INT
from src.middleware.database import Base, DatabaseClient
from src.registry.abstract_repository import AbstractCreate, AbstractModel, AbstractQuery, AbstractRepository

logger = getLogger(__name__)


class AnimalSubcategory(Base):
    __tablename__ = "animal_subcategories"
    id = Column(
        String(32),
        primary_key=True,
    )
    name = Column(
        String(128),
        nullable=False,
        unique=False,
    )
