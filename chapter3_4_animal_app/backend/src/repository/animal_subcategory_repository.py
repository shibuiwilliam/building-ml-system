from logging import getLogger
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
from src.middleware.database import Base
from src.repository.abstract_repository import AbstractRepository
from src.repository.animal_category_repository import AnimalCategory
from src.schema.animal_subcategory import AnimalSubcategoryCreate, AnimalSubcategoryModel, AnimalSubcategoryQuery
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


class AnimalSubcategoryRepository(AbstractRepository):
    def __init__(self) -> None:
        super().__init__()
        self.table_name = TABLES.ANIMAL_SUBCATEGORY.value

    def select(
        self,
        session: Session,
        query: Optional[AnimalSubcategoryQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalSubcategoryModel]:
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(AnimalSubcategory.id == query.id)
            if query.animal_category_id is not None:
                filters.append(AnimalCategory.id == query.animal_category_id)
            if query.name is not None:
                filters.append(AnimalSubcategory.name == query.name)
            if query.is_deleted is not None:
                filters.append(AnimalSubcategory.is_deleted == query.is_deleted)
        results = (
            session.query(
                AnimalSubcategory.id.label("id"),
                AnimalSubcategory.name.label("name"),
                AnimalCategory.id.label("animal_category_id"),
                AnimalCategory.name.label("animal_category_name"),
                AnimalSubcategory.is_deleted.label("is_deleted"),
                AnimalSubcategory.created_at.label("created_at"),
                AnimalSubcategory.updated_at.label("updated_at"),
            )
            .join(
                AnimalCategory,
                AnimalCategory.id == AnimalSubcategory.animal_category_id,
                isouter=True,
            )
            .filter(and_(*filters))
            .order_by(AnimalSubcategory.id)
            .all()
        )
        data = [AnimalSubcategoryModel(**(self.model_to_dict(d))) for d in results]
        return data

    def insert(
        self,
        session: Session,
        record: AnimalSubcategoryCreate,
        commit: bool = True,
    ) -> Optional[AnimalSubcategoryModel]:
        data = AnimalSubcategory(**record.dict())
        session.add(data)
        if commit:
            session.commit()
            session.refresh(data)
            result = self.select(
                session=session,
                query=AnimalSubcategoryQuery(id=data.id),
            )
            return result[0]
        return None
