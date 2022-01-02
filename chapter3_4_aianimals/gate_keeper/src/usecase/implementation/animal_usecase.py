from typing import Dict

from src.entities.animal import ANIMAL_MAPPING, ANIMAL_MAPPING_NAME, AnimalDocument, AnimalQuery
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.usecase.animal_usecase import AbstractAnimalUsecase

logger = configure_logger(__name__)


class AnimalUsecase(AbstractAnimalUsecase):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
    ):
        super().__init__(animal_repository=animal_repository)

    def create_index(self):
        self.animal_repository.create_index(
            index=ANIMAL_MAPPING_NAME,
            body=ANIMAL_MAPPING,
        )

    def get_index(self) -> Dict:
        return self.animal_repository.get_index()

    def index_exists(self) -> bool:
        return self.animal_repository.index_exists()

    def register_index(self):
        animal_id = self.animal_repository.dequeue()
        if animal_id is None:
            return
        logger.info(f"animal_id: {animal_id}")
        query = AnimalQuery(
            id=animal_id,
            deactivated=False,
        )
        animals = self.animal_repository.select(
            query=query,
            limit=1,
            offset=0,
        )
        if len(animals) == 0:
            return
        animal = animals[0]
        document = AnimalDocument(
            name=animal.name,
            description=animal.description,
            animal_category_name_en=animal.animal_category_name_en,
            animal_category_name_ja=animal.animal_category_name_ja,
            animal_subcategory_name_en=animal.animal_subcategory_name_en,
            animal_subcategory_name_ja=animal.animal_subcategory_name_ja,
            photo_url=animal.photo_url,
            user_handle_name=animal.user_handle_name,
            created_at=animal.created_at,
        )
        self.animal_repository.create_document(
            id=animal.id,
            document=document,
            index=ANIMAL_MAPPING_NAME,
        )
        logger.info(f"registered: {animal_id}")
