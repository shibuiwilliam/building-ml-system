from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.entities.animal_subcategory import AnimalSubcategoryCreate, AnimalSubcategoryModel, AnimalSubcategoryQuery
from src.schema.animal_category import AnimalCategory
from src.schema.animal_subcategory import AnimalSubcategory
from src.schema.table import TABLES

logger = getLogger(__name__)


class AbstractAnimalSubcategoryRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[AnimalSubcategoryQuery],
    ) -> List[AnimalSubcategoryModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: AnimalSubcategoryCreate,
        commit: bool = True,
    ) -> Optional[AnimalSubcategoryModel]:
        raise NotImplementedError


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
                filters.append(AnimalCategory.id == query.animal_category_id)
            if query.name_en is not None:
                filters.append(AnimalSubcategory.name_en == query.name_en)
            if query.name_ja is not None:
                filters.append(AnimalSubcategory.name_ja == query.name_ja)
            if query.is_deleted is not None:
                filters.append(AnimalSubcategory.is_deleted == query.is_deleted)
        results = (
            session.query(
                AnimalSubcategory.id.label("id"),
                AnimalSubcategory.name_en.label("name_en"),
                AnimalSubcategory.name_ja.label("name_ja"),
                AnimalCategory.id.label("animal_category_id"),
                AnimalCategory.name_en.label("animal_category_name_en"),
                AnimalCategory.name_ja.label("animal_category_name_ja"),
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
        data = [
            AnimalSubcategoryModel(
                id=d[0],
                name_en=d[1],
                name_ja=d[2],
                animal_category_id=d[3],
                animal_category_name_en=d[4],
                animal_category_name_ja=d[5],
                is_deleted=d[6],
                created_at=d[7],
                updated_at=d[8],
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
