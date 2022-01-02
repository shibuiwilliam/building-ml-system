from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.animal import AnimalCreate, AnimalQuery
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
        session: Session,
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
            session=session,
            query=query,
            limit=limit,
            offset=offset,
        )
        response = [AnimalResponseWithLike(**d.dict()) for d in data]
        return response

    def register(
        self,
        session: Session,
        request: AnimalCreateRequest,
    ) -> Optional[AnimalResponse]:
        logger.info(f"register: {request}")
        exists = self.animal_repository.select(
            session=session,
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
            session=session,
            record=record,
            commit=True,
        )
        if data is not None:
            response = AnimalResponse(**data.dict())
            self.queue.enqueue(
                queue_name="animal",
                key=data.id,
            )
            logger.info(f"done register: {response}")
            return response
        return None
