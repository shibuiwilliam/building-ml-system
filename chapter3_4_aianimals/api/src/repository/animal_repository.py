from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.entities.animal import AnimalCreate, AnimalModel, AnimalQuery
from src.entities.user import UserModel
from src.schema.animal import Animal
from src.schema.animal_category import AnimalCategory
from src.schema.animal_subcategory import AnimalSubcategory
from src.schema.like import Like
from src.schema.table import TABLES
from src.schema.user import User

logger = getLogger(__name__)


class AbstractAnimalRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[AnimalQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalModel]:
        raise NotImplementedError

    @abstractmethod
    def liked_by(
        self,
        session: Session,
        animal_id: str,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[UserModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: AnimalCreate,
        commit: bool = True,
    ) -> Optional[AnimalModel]:
        raise NotImplementedError


class AnimalRepository(AbstractAnimalRepository):
    def __init__(self) -> None:
        super().__init__()
        self.table_name = TABLES.ANIMAL.value

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
                filters.append(Animal.animal_category_id == query.animal_category_id)
            if query.animal_subcategory_id is not None:
                filters.append(Animal.animal_subcategory_id == query.animal_subcategory_id)
            if query.user_id is not None:
                filters.append(User.id == query.user_id)
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
                User.id.label("user_id"),
                User.handle_name.label("user_handle_name"),
                Animal.name.label("name"),
                Animal.description.label("description"),
                Animal.photo_url.label("photo_url"),
                Animal.deactivated.label("deactivated"),
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
                user_id=d[7],
                user_handle_name=d[8],
                name=d[9],
                description=d[10],
                photo_url=d[11],
                deactivated=d[12],
                created_at=d[13],
                updated_at=d[14],
            )
            for d in results
        ]
        return data

    def liked_by(
        self,
        session: Session,
        animal_id: str,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[UserModel]:
        results = (
            session.query(User)
            .join(
                Like,
                Like.user_id == User.id,
                isouter=True,
            )
            .join(
                Animal,
                Animal.id == Like.animal_id,
                isouter=True,
            )
            .filter(Animal.id == animal_id)
            .order_by(User.id)
            .limit(limit)
            .offset(offset)
        )
        data = [
            UserModel(
                id=d.id,
                handle_name=d.handle_name,
                email_address=d.email_address,
                age=d.age,
                gender=d.gender,
                deactivated=d.deactivated,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in results
        ]
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
                query=AnimalQuery(id=data.id),
                limit=1,
                offset=0,
            )
            return result[0]
        return None
