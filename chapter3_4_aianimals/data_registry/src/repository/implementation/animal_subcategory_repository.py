from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.entities.animal_subcategory import AnimalSubcategoryCreate, AnimalSubcategoryModel, AnimalSubcategoryQuery
from src.middleware.logger import configure_logger
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository
from src.schema.animal_subcategory import AnimalSubcategory
from src.schema.table import TABLES

logger = configure_logger(__name__)


class AnimalSubcategoryRepository(AbstractAnimalSubcategoryRepository):
    def __init__(self):
        super().__init__()
        self.table_name = TABLES.ANIMAL_SUBCATEGORY.value

    def select(
        self,
        session: Session,
        query: Optional[AnimalSubcategoryQuery],
    ) -> List[AnimalSubcategoryModel]:
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(AnimalSubcategory.id == query.id)
            if query.animal_category_id is not None:
                filters.append(AnimalSubcategory.id == query.animal_category_id)
            if query.name is not None:
                filters.append(AnimalSubcategory.name == query.name)
            if query.is_deleted is not None:
                filters.append(AnimalSubcategory.is_deleted == query.is_deleted)
        results = session.query(AnimalSubcategory).filter(and_(*filters)).order_by(AnimalSubcategory.id).all()
        data = [
            AnimalSubcategoryModel(
                id=d.id,
                name=d.name,
                animal_category_id=d.animal_category_id,
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
