from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import INT
from src.infrastructure.postgresql_database import PostgreSQLDatabase
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class TABLES(Enum):
    ANIMAL_CATEGORY = "animal_categories"
    ANIMAL_SUBCATEGORY = "animal_subcategories"
    ANIMAL = "animals"
    USER = "users"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in TABLES.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in TABLES.__members__.values()]


Base = declarative_base()


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
        INT,
        ForeignKey(f"{TABLES.ANIMAL_CATEGORY.value}.id"),
        nullable=False,
        unique=False,
    )
    animal_subcategory_id = Column(
        INT,
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


class AnimalQuery(BaseModel):
    id: Optional[str]
    name: Optional[str]
    animal_category_id: Optional[int]
    animal_subcategory_id: Optional[int]
    deactivated: Optional[bool]

    class Config:
        extra = Extra.forbid


class AnimalModel(BaseModel):
    id: str
    animal_category_id: int
    animal_subcategory_id: int
    name: str
    description: str
    photo_url: str
    deactivated: bool = False
    user_id: str
    created_at: datetime
    updated_at: datetime


class AnimalRepository(object):
    def __init__(self, database: PostgreSQLDatabase) -> None:
        self.database = database

    def select(
        self,
        query: Optional[AnimalQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalModel]:
        session = self.database.get_session().__next__()
        try:
            filters = []
            if query is not None:
                if query.id is not None:
                    filters.append(Animal.id == query.id)
                if query.name is not None:
                    filters.append(Animal.name == query.name)
                if query.animal_category_id is not None:
                    filters.append(Animal.animal_category_id == query.animal_category_id)
                if query.animal_subcategory_id is not None:
                    filters.append(Animal.animal_subcategory_id == query.animal_subcategory_id)
                if query.deactivated is not None:
                    filters.append(Animal.deactivated == query.deactivated)
            results = session.query(Animal).filter(and_(*filters)).order_by(Animal.id).limit(limit).offset(offset)
            data = [
                AnimalModel(
                    id=d.id,
                    animal_category_id=d.animal_category_id,
                    animal_subcategory_id=d.animal_subcategory_id,
                    name=d.name,
                    description=d.description,
                    photo_url=d.photo_url,
                    deactivated=d.deactivated,
                    user_id=d.user_id,
                    created_at=d.created_at,
                    updated_at=d.updated_at,
                )
                for d in results
            ]
            return data
        except Exception as e:
            raise e
        finally:
            session.close()
