from typing import List, Optional

from sqlalchemy import and_
from src.entities.animal_subcategory import AnimalSubcategoryCreate, AnimalSubcategoryModel, AnimalSubcategoryQuery
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository
from src.schema.animal_subcategory import AnimalSubcategory
from src.schema.table import TABLES

logger = configure_logger(__name__)


class AnimalSubcategoryRepository(AbstractAnimalSubcategoryRepository):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        super().__init__(database=database)
        self.table_name = TABLES.ANIMAL_SUBCATEGORY.value

    def select(
        self,
        query: Optional[AnimalSubcategoryQuery],
    ) -> List[AnimalSubcategoryModel]:
        session = self.database.get_session().__next__()
        try:
            filters = []
            if query is not None:
                if query.id is not None:
                    filters.append(AnimalSubcategory.id == query.id)
                if query.animal_category_id is not None:
                    filters.append(AnimalSubcategory.id == query.animal_category_id)
                if query.name_en is not None:
                    filters.append(AnimalSubcategory.name_en == query.name_en)
                if query.name_ja is not None:
                    filters.append(AnimalSubcategory.name_ja == query.name_ja)
                if query.is_deleted is not None:
                    filters.append(AnimalSubcategory.is_deleted == query.is_deleted)
            results = session.query(AnimalSubcategory).filter(and_(*filters)).order_by(AnimalSubcategory.id).all()
            data = [
                AnimalSubcategoryModel(
                    id=d.id,
                    name_en=d.name_en,
                    name_ja=d.name_ja,
                    animal_category_id=d.animal_category_id,
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
        record: AnimalSubcategoryCreate,
        commit: bool = True,
    ) -> Optional[AnimalSubcategoryModel]:
        session = self.database.get_session().__next__()
        try:
            data = AnimalSubcategory(**record.dict())
            session.add(data)
            if commit:
                session.commit()
                session.refresh(data)
                result = self.select(query=AnimalSubcategoryQuery(id=data.id))
                session.close()
                return result[0]
            return None
        except Exception as e:
            raise e
        finally:
            session.close()
