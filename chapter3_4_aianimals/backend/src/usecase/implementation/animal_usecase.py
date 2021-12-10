from logging import getLogger
from typing import List, Optional

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from src.entities.animal import AnimalCreate, AnimalQuery
from src.infrastructure.queue import AbstractQueue
from src.infrastructure.storage import AbstractStorage
from src.middleware.strings import get_uuid
from src.repository.animal_repository import AbstractAnimalRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest
from src.response_object.animal import AnimalResponse, AnimalResponseWithLike
from src.response_object.user import UserResponse
from src.usecase.animal_usecase import AbstractAnimalUsecase

logger = getLogger(__name__)


class AnimalUsecase(AbstractAnimalUsecase):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        storage_client: AbstractStorage,
        queue: AbstractQueue,
    ):
        super().__init__(
            animal_repository=animal_repository,
            storage_client=storage_client,
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
        data = self.animal_repository.select_with_like(
            session=session,
            query=query,
            limit=limit,
            offset=offset,
        )
        response = [AnimalResponseWithLike(**d.dict()) for d in data]
        return response

    def liked_by(
        self,
        session: Session,
        animal_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[UserResponse]:
        if limit > 200:
            raise ValueError
        data = self.animal_repository.liked_by(
            session=session,
            animal_id=animal_id,
            limit=limit,
            offset=offset,
        )
        response = [UserResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        session: Session,
        request: AnimalCreateRequest,
        local_file_path: str,
        background_tasks: BackgroundTasks,
    ) -> Optional[AnimalResponse]:
        id = get_uuid()
        photo_url = self.storage_client.make_photo_url(uuid=id)
        background_tasks.add_task(
            self.storage_client.upload_image,
            id,
            local_file_path,
        )
        logger.info(f"uploaded image to {photo_url}")
        record = AnimalCreate(
            id=id,
            animal_category_id=request.animal_category_id,
            animal_subcategory_id=request.animal_subcategory_id,
            user_id=request.user_id,
            name=request.name,
            description=request.description,
            photo_url=photo_url,
        )
        data = self.animal_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        if data is not None:
            response = AnimalResponse(**data.dict())
            background_tasks.add_task(
                self.queue.enqueue,
                "animal",
                data.id,
            )
            return response
        return None
