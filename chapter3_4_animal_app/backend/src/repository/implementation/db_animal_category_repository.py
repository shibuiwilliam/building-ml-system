from logging import getLogger
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.repository.animal_category_repository import AnimalCategoryRepository
from src.entities.animal_category import AnimalCategoryQuery, AnimalCategoryModel, AnimalCategoryCreate
from src.schema.animal_category import AnimalCategory
from src.schema.table import TABLES

logger = getLogger(__name__)


class DBAnimalCategoryRepository(AnimalCategoryRepository):
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
        data = [AnimalCategoryModel(**(DBAnimalCategoryRepository.model_to_dict(d))) for d in results]
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
