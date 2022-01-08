from typing import Dict, List, Optional

from src.configurations import Configurations
from src.entities.animal import ANIMAL_MAPPING, ANIMAL_MAPPING_NAME, AnimalCreate, AnimalDocument, AnimalQuery
from src.infrastructure.queue import AbstractQueue
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest
from src.response_object.animal import AnimalResponse, AnimalResponseWithLike
from src.usecase.animal_usecase import AbstractAnimalUsecase

logger = configure_logger(__name__)


class AnimalUsecase(AbstractAnimalUsecase):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        queue: AbstractQueue,
    ):
        super().__init__(
            animal_repository=animal_repository,
            queue=queue,
        )

    def retrieve(
        self,
        request: Optional[AnimalRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AnimalResponseWithLike]:
        if limit > 200:
            raise ValueError
        query: Optional[AnimalQuery] = None
        if request is not None:
            query = AnimalQuery(**request.dict())
        data = self.animal_repository.select(
            query=query,
            limit=limit,
            offset=offset,
        )
        response = [AnimalResponseWithLike(**d.dict()) for d in data]
        return response

    def register(
        self,
        request: AnimalCreateRequest,
    ) -> Optional[AnimalResponse]:
        logger.info(f"register: {request}")
        exists = self.animal_repository.select(
            query=AnimalQuery(id=request.id),
        )
        if len(exists) > 0:
            response = AnimalResponse(**exists[0].dict())
            logger.info(f"data already exists: {response}")
            return response

        record = AnimalCreate(
            id=request.id,
            animal_category_id=request.animal_category_id,
            animal_subcategory_id=request.animal_subcategory_id,
            user_id=request.user_id,
            name=request.name,
            description=request.description,
            photo_url=request.photo_url,
            created_at=request.created_at,
        )
        data = self.animal_repository.insert(
            record=record,
            commit=True,
        )
        if data is not None:
            response = AnimalResponse(**data.dict())
            self.queue.enqueue(
                queue_name=Configurations.animal_registry_queue,
                key=data.id,
            )
            logger.info(f"done register: {response}")
            return response
        return None

    def create_index(self):
        self.animal_repository.create_index(
            index=ANIMAL_MAPPING_NAME,
            body=ANIMAL_MAPPING,
        )

    def get_index(self) -> Dict:
        return self.animal_repository.get_index()

    def index_exists(self) -> bool:
        return self.animal_repository.index_exists()

    def register_index(
        self,
        animal_id: str,
    ):
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

    def register_index_from_queue(self):
        animal_id = self.queue.dequeue(queue_name=Configurations.animal_registry_queue)
        if animal_id is None:
            return
        self.register_index(animal_id=animal_id)
