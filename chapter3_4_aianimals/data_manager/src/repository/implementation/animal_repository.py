from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.entities.animal import AnimalCreate, AnimalModel, AnimalQuery
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.schema.animal import Animal
from src.schema.table import TABLES

logger = configure_logger(__name__)


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
                filters.append(Animal.animal_category_id == query.animal_category_id)
            if query.animal_subcategory_id is not None:
                filters.append(Animal.animal_subcategory_id == query.animal_subcategory_id)
            if query.user_id is not None:
                filters.append(Animal.id == query.user_id)
            if query.deactivated is not None:
                filters.append(Animal.deactivated == query.deactivated)
        results = session.query(Animal).filter(and_(*filters)).order_by(Animal.id).limit(limit).offset(offset)
        data = [
            AnimalModel(
                id=d.id,
                animal_category_id=d.animal_category_id,
                animal_subcategory_id=d.animal_subcategory_id,
                user_id=d.user_id,
                name=d.name,
                description=d.description,
                photo_url=d.photo_url,
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
