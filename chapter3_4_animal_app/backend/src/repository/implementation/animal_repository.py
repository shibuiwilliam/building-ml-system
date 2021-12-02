from logging import getLogger
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.func import count
from sqlalchemy.orm import Session
from src.entities.animal import AnimalCreate, AnimalModel, AnimalModelWithLike, AnimalQuery
from src.repository.animal_repository import AbstractAnimalRepository
from src.schema.animal import Animal
from src.schema.animal_category import AnimalCategory
from src.schema.animal_subcategory import AnimalSubcategory
from src.schema.like import Like
from src.schema.table import TABLES
from src.schema.user import User

logger = getLogger(__name__)


class AnimalRepository(AbstractAnimalRepository):
    def __init__(self) -> None:
        super().__init__()
        self.table_name = TABLES.USER.value

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
                filters.append(AnimalCategory.id == query.animal_category_id)
            if query.animal_subcategory_id is not None:
                filters.append(AnimalSubcategory.id == query.animal_subcategory_id)
            if query.user_id is not None:
                filters.append(User.id == query.user_id)
            if query.deactivated is not None:
                filters.append(Animal.deactivated == query.deactivated)
        results = (
            session.query(
                Animal.id.label("id"),
                AnimalCategory.id.label("animal_category_id"),
                AnimalCategory.name.label("animal_category_name"),
                AnimalSubcategory.id.label("animal_subcategory_id"),
                AnimalSubcategory.name.label("animal_subcategory_name"),
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
        data = [AnimalModel(**(AnimalRepository.model_to_dict(d))) for d in results]
        return data

    def select_with_like(
        self,
        session: Session,
        query: Optional[AnimalQuery],
        order_by_like: bool = True,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalModelWithLike]:
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(Animal.id == query.id)
            if query.name is not None:
                filters.append(Animal.name == query.name)
            if query.animal_category_id is not None:
                filters.append(AnimalCategory.id == query.animal_category_id)
            if query.animal_subcategory_id is not None:
                filters.append(AnimalSubcategory.id == query.animal_subcategory_id)
            if query.user_id is not None:
                filters.append(User.id == query.user_id)
            if query.deactivated is not None:
                filters.append(Animal.deactivated == query.deactivated)
        results = (
            session.query(
                Animal.id.label("id"),
                AnimalCategory.id.label("animal_category_id"),
                AnimalCategory.name.label("animal_category_name"),
                AnimalSubcategory.id.label("animal_subcategory_id"),
                AnimalSubcategory.name.label("animal_subcategory_name"),
                User.id.label("user_id"),
                User.handle_name.label("user_handle_name"),
                Animal.name.label("name"),
                Animal.description.label("description"),
                Animal.photo_url.label("photo_url"),
                Animal.deactivated.label("deactivated"),
                Animal.created_at.label("created_at"),
                Animal.updated_at.label("updated_at"),
                count(Like.id).label("like"),
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
            .join(
                Like,
                Like.animal_id == Animal.id,
                isouter=True,
            )
            .filter(and_(*filters))
            .group_by(Like.animal_id)
            .order_by("like" if order_by_like else Animal.id)
            .limit(limit)
            .offset(offset)
        )
        data = [AnimalModelWithLike(**(AnimalRepository.model_to_dict(d))) for d in results]
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
                query=AnimalQuery(
                    id=data.id,
                    limit=1,
                    offset=0,
                ),
            )
            return result[0]
        return None
