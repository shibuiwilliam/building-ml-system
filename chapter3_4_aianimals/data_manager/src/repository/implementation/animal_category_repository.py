from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.entities.animal_category import AnimalCategoryCreate, AnimalCategoryModel, AnimalCategoryQuery
from src.middleware.logger import configure_logger
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.schema.animal_category import AnimalCategory
from src.schema.table import TABLES

logger = configure_logger(__name__)


class AnimalCategoryRepository(AbstractAnimalCategoryRepository):
    def __init__(self):
        super().__init__()
        self.table_name = TABLES.ANIMAL_CATEGORY.value

    def select(
        self,
        session: Session,
        query: Optional[AnimalCategoryQuery],
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
        data = [
            AnimalCategoryModel(
                id=d.id,
                name=d.name,
                is_deleted=d.is_deleted,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in results
        ]
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
