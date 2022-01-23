from typing import Optional

from src.entities.animal import AnimalModel, AnimalUpdate
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.schema.animal import Animal

logger = configure_logger(__name__)


class AnimalRepository(AbstractAnimalRepository):
    def __init__(self, database: AbstractDatabase) -> None:
        super().__init__(database=database)

    def update(
        self,
        record: AnimalUpdate,
    ) -> Optional[AnimalModel]:
        session = self.database.get_session().__next__()
        try:
            session.query(Animal).filter(Animal.id == record.id).update({"deactivated": record.deactivated})
            session.commit()
            _data = session.query(Animal).filter(Animal.id == record.id).first()
            data = AnimalModel(
                id=_data.id,
                animal_category_id=_data.animal_category_id,
                animal_subcategory_id=_data.animal_subcategory_id,
                name=_data.name,
                description=_data.description,
                photo_url=_data.photo_url,
                deactivated=_data.deactivated,
                user_id=_data.user_id,
                created_at=_data.created_at,
                updated_at=_data.updated_at,
            )
            return data
        except Exception as e:
            raise e
        finally:
            session.close()
