from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy import and_
from src.entities.animal import AnimalCreate, AnimalModel, AnimalQuery, AnimalUpdate
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger
from src.schema.animal import Animal
from src.schema.animal_category import AnimalCategory
from src.schema.animal_subcategory import AnimalSubcategory
from src.schema.user import User

logger = configure_logger(__name__)


class AbstractAnimalRepository(ABC):
    def __init__(self, database: AbstractDatabase):
        self.database = database

    @abstractmethod
    def select(
        self,
        query: Optional[AnimalQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        record: AnimalCreate,
        commit: bool = True,
    ) -> Optional[AnimalModel]:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        record: AnimalUpdate,
    ):
        raise NotImplementedError

    @abstractmethod
    def bulk_insert(
        self,
        records: List[AnimalCreate],
        commit: bool = True,
    ):
        raise NotImplementedError


class AnimalRepository(AbstractAnimalRepository):
    def __init__(self, database: AbstractDatabase) -> None:
        super().__init__(database=database)

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
                if query.ids is not None:
                    filters.append(Animal.id.in_(query.ids))
                if query.name is not None:
                    filters.append(Animal.name == query.name)
                if query.animal_category_id is not None:
                    filters.append(Animal.animal_category_id == query.animal_category_id)
                if query.animal_subcategory_id is not None:
                    filters.append(Animal.animal_subcategory_id == query.animal_subcategory_id)
                if query.user_id is not None:
                    filters.append(Animal.id == query.user_id)
                if query.deactivated is not None:
                    filters.append(Animal.deactivated == query.deactivated)
            results = (
                session.query(
                    Animal.id.label("id"),
                    AnimalCategory.id.label("animal_category_id"),
                    AnimalCategory.name_en.label("animal_category_name_en"),
                    AnimalCategory.name_ja.label("animal_category_name_ja"),
                    AnimalSubcategory.id.label("animal_subcategory_id"),
                    AnimalSubcategory.name_en.label("animal_subcategory_name_en"),
                    AnimalSubcategory.name_ja.label("animal_subcategory_name_ja"),
                    Animal.name.label("name"),
                    Animal.description.label("description"),
                    Animal.photo_url.label("photo_url"),
                    Animal.deactivated.label("deactivated"),
                    User.id.label("user_id"),
                    User.handle_name.label("user_handle_name"),
                    Animal.created_at.label("created_at"),
                    Animal.updated_at.label("updated_at"),
                )
                .join(
                    AnimalCategory,
                    AnimalCategory.id == Animal.animal_category_id,
                    isouter=True,
                )
                .join(
                    AnimalSubcategory,
                    AnimalSubcategory.id == Animal.animal_subcategory_id,
                    isouter=True,
                )
                .join(
                    User,
                    User.id == Animal.user_id,
                    isouter=True,
                )
                .filter(and_(*filters))
                .order_by(Animal.id)
                .limit(limit)
                .offset(offset)
            )
            data = [
                AnimalModel(
                    id=d[0],
                    animal_category_id=d[1],
                    animal_category_name_en=d[2],
                    animal_category_name_ja=d[3],
                    animal_subcategory_id=d[4],
                    animal_subcategory_name_en=d[5],
                    animal_subcategory_name_ja=d[6],
                    name=d[7],
                    description=d[8],
                    photo_url=d[9],
                    deactivated=d[10],
                    user_id=d[11],
                    user_handle_name=d[12],
                    created_at=d[13],
                    updated_at=d[14],
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
        record: AnimalCreate,
        commit: bool = True,
    ) -> Optional[AnimalModel]:
        session = self.database.get_session().__next__()
        try:
            data = Animal(**record.dict())
            session.add(data)
            if commit:
                session.commit()
                session.refresh(data)
                result = self.select(
                    query=AnimalQuery(id=data.id),
                    limit=1,
                    offset=0,
                )
                session.close()
                return result[0]
            return None
        except Exception as e:
            raise e
        finally:
            session.close()

    def update(
        self,
        record: AnimalUpdate,
    ):
        session = self.database.get_session().__next__()
        try:
            updates = {}
            if record.name is not None:
                updates["name"] = record.name
            if record.animal_category_id is not None:
                updates["animal_category_id"] = record.animal_category_id
            if record.animal_subcategory_id is not None:
                updates["animal_subcategory_id"] = record.animal_subcategory_id
            if record.user_id is not None:
                updates["user_id"] = record.user_id
            if record.description is not None:
                updates["description"] = record.description
            if record.photo_url is not None:
                updates["photo_url"] = record.photo_url
            if record.deactivated is not None:
                updates["deactivated"] = record.deactivated
            session.query(Animal).filter(Animal.id == record.id).update(updates)
            session.commit()
        except Exception as e:
            raise e
        finally:
            session.close()

    def bulk_insert(
        self,
        records: List[AnimalCreate],
        commit: bool = True,
    ):
        session = self.database.get_session().__next__()
        try:
            data = [d.dict() for d in records]
            session.execute(Animal.__table__.insert(), data)
            if commit:
                session.commit()
        except Exception as e:
            raise e
        finally:
            session.close()
