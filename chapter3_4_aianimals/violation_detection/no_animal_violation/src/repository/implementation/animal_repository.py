from typing import List, Optional

from sqlalchemy import and_
from src.entities.animal import AnimalModel, AnimalQuery
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.schema.animal import Animal

logger = configure_logger(__name__)


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
            results = session.query(Animal).filter(and_(*filters)).order_by(Animal.id).limit(limit).offset(offset)
            data = [
                AnimalModel(
                    id=d.id,
                    animal_category_id=d.animal_category_id,
                    animal_subcategory_id=d.animal_subcategory_id,
                    name=d.name,
                    description=d.description,
                    photo_url=d.photo_url,
                    deactivated=d.deactivated,
                    user_id=d.user_id,
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
