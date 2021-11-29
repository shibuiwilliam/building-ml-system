from logging import getLogger
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, String, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
from src.middleware.database import Base
from src.repository.abstract_repository import AbstractRepository
from src.schema.animal_category import AnimalCategoryCreate, AnimalCategoryModel, AnimalCategoryQuery
from src.schema.table import TABLES

logger = getLogger(__name__)


class AnimalCategory(Base):
    __tablename__ = TABLES.ANIMAL_CATEGORY.value
    id = Column(
        String(32),
        primary_key=True,
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


class AnimalCategoryRepository(AbstractRepository):
    def __init__(self) -> None:
        super().__init__()
        self.table_name = TABLES.ANIMAL_CATEGORY.value

    def select(
        self,
        session: Session,
        query: Optional[AnimalCategoryQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalCategoryModel]:
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(AnimalCategory.id == query.id)
            if query.name is not None:
                filters.append(AnimalCategory.name == query.name)
            if query.is_deleted is not None:
                filters.append(AnimalCategory.is_deleted == query.is_deleted)
        results = session.query(AnimalCategory).filter(and_(*filters)).order_by(AnimalCategory.id).all()
        data = [AnimalCategoryModel(**(self.model_to_dict(d))) for d in results]
        return data

    def insert(
        self,
        session: Session,
        record: AnimalCategoryCreate,
        commit: bool = True,
    ) -> Optional[AnimalCategoryModel]:
        data = AnimalCategory(**record.dict())
        session.add(data)
        if commit:
            session.commit()
            session.refresh(data)
            result = self.select(
                session=session,
                query=AnimalCategoryQuery(id=data.id),
            )
            return result[0]
        return None
