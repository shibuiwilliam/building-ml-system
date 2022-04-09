import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy import and_
from src.entities.animal_category import AnimalCategoryCreate, AnimalCategoryModel, AnimalCategoryQuery
from src.infrastructure.database import AbstractDatabase
from src.schema.animal_category import AnimalCategory
from src.schema.table import TABLES


class AbstractAnimalCategoryRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.logger = logging.getLogger(__name__)
        self.database = database

    @abstractmethod
    def select(
        self,
        query: Optional[AnimalCategoryQuery],
    ) -> List[AnimalCategoryModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        record: AnimalCategoryCreate,
        commit: bool = True,
    ) -> Optional[AnimalCategoryModel]:
        raise NotImplementedError


class AnimalCategoryRepository(AbstractAnimalCategoryRepository):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        super().__init__(database=database)
        self.table_name = TABLES.ANIMAL_CATEGORY.value

    def select(
        self,
        query: Optional[AnimalCategoryQuery],
    ) -> List[AnimalCategoryModel]:
        session = self.database.get_session().__next__()
        try:
            filters = []
            if query is not None:
                if query.id is not None:
                    filters.append(AnimalCategory.id == query.id)
                if query.name_en is not None:
                    filters.append(AnimalCategory.name_en == query.name_en)
                if query.name_ja is not None:
                    filters.append(AnimalCategory.name_ja == query.name_ja)
                if query.is_deleted is not None:
                    filters.append(AnimalCategory.is_deleted == query.is_deleted)
            results = session.query(AnimalCategory).filter(and_(*filters)).order_by(AnimalCategory.id).all()
            data = [
                AnimalCategoryModel(
                    id=d.id,
                    name_en=d.name_en,
                    name_ja=d.name_ja,
                    is_deleted=d.is_deleted,
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

    def insert(
        self,
        record: AnimalCategoryCreate,
        commit: bool = True,
    ) -> Optional[AnimalCategoryModel]:
        session = self.database.get_session().__next__()
        try:
            data = AnimalCategory(**record.dict())
            session.add(data)
            if commit:
                session.commit()
                session.refresh(data)
                result = self.select(query=AnimalCategoryQuery(id=data.id))
                return result[0]
            return None
        except Exception as e:
            raise e
        finally:
            session.close()
