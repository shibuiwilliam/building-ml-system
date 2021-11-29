from logging import getLogger
from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import Boolean
from src.middleware.database import Base
from src.repository.abstract_repository import AbstractRepository
from src.repository.animal_category_repository import AnimalCategory
from src.repository.animal_subcategory_repository import AnimalSubcategory
from src.repository.user_repository import User
from src.schema.animal import AnimalCreate, AnimalModel, AnimalQuery
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


class AnimalRepository(AbstractRepository):
    def __init__(self) -> None:
        super().__init__()
        self.table_name = TABLES.USER.value

    def select(
        self,
        session: Session,
        query: Optional[AnimalQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalModel]:
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(Animal.id == query.id)
            if query.name is not None:
                filters.append(Animal.name == query.name)
            if query.animal_category_id is not None:
                filters.append(AnimalCategory.id == query.animal_category_id)
            if query.animal_subcategory_id is not None:
                filters.append(AnimalSubcategory.id == query.animal_subcategory_id)
            if query.user_id is not None:
                filters.append(User.id == query.user_id)
            if query.deactivated is not None:
                filters.append(Animal.deactivated == query.deactivated)
        results = (
            session.query(
                Animal.id.label("id"),
                AnimalCategory.id.label("animal_category_id"),
                AnimalCategory.name.label("animal_category_name"),
                AnimalSubcategory.id.label("animal_subcategory_id"),
                AnimalSubcategory.name.label("animal_subcategory_name"),
                User.id.label("user_id"),
                User.handle_name.label("user_handle_name"),
                Animal.name.label("name"),
                Animal.description.label("description"),
                Animal.photo_url.label("photo_url"),
                Animal.deactivated.label("deactivated"),
                Animal.created_at.label("created_at"),
                Animal.updated_at.label("updated_at"),
            )
            .filter(and_(*filters))
            .order_by(Animal.id)
            .limit(limit)
            .offset(offset)
        )
        data = [AnimalModel(**(self.model_to_dict(d))) for d in results]
        return data

    def insert(
        self,
        session: Session,
        record: AnimalCreate,
        commit: bool = True,
    ) -> Optional[AnimalModel]:
        data = Animal(**record.dict())
        session.add(data)
        if commit:
            session.commit()
            session.refresh(data)
            result = self.select(
                session=session,
                query=AnimalQuery(
                    id=data.id,
                    limit=1,
                    offset=0,
                ),
            )
            return result[0]
        return None
