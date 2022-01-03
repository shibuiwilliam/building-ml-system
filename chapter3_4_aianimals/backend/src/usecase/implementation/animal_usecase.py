from logging import getLogger
from typing import List, Optional

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from src.entities.animal import AnimalCreate, AnimalQuery, AnimalSearchQuery
from src.infrastructure.queue import AbstractQueue
from src.infrastructure.storage import AbstractStorage
from src.middleware.strings import get_uuid
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.animal_search_repository import AbstractAnimalSearchRepository
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest, AnimalSearchRequest
from src.response_object.animal import AnimalResponse, AnimalSearchResponse, AnimalSearchResponses
from src.response_object.user import UserResponse
from src.usecase.animal_usecase import AbstractAnimalUsecase

logger = getLogger(__name__)


class AnimalUsecase(AbstractAnimalUsecase):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        animal_search_repository: AbstractAnimalSearchRepository,
        like_repository: AbstractLikeRepository,
        storage_client: AbstractStorage,
        queue: AbstractQueue,
    ):
        super().__init__(
            animal_repository=animal_repository,
            animal_search_repository=animal_search_repository,
            like_repository=like_repository,
            storage_client=storage_client,
            queue=queue,
        )

    def retrieve(
        self,
        session: Session,
        request: Optional[AnimalRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AnimalResponse]:
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
        likes = self.like_repository.count(
            session=session,
            animal_ids=[a.id for a in data],
        )
        response = [AnimalResponse(likes=likes[d.id].count, **d.dict()) for d in data]
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

    def search(
        self,
        session: Session,
        request: Optional[AnimalSearchRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> AnimalSearchResponses:
        query: Optional[AnimalSearchQuery] = None
        if request is not None:
            query = AnimalSearchQuery(
                animal_category_name_en=request.animal_category_name_en,
                animal_category_name_ja=request.animal_category_name_ja,
                animal_subcategory_name_en=request.animal_subcategory_name_en,
                animal_subcategory_name_ja=request.animal_subcategory_name_ja,
                phrases=request.phrases,
            )
        results = self.animal_search_repository.search(
            query=query,
            from_=offset,
            size=limit,
        )
        animal_ids = [r.id for r in results.results]
        likes = self.like_repository.count(
            session=session,
            animal_ids=animal_ids,
        )
        searched = AnimalSearchResponses(
            hits=results.hits,
            max_score=results.max_score,
            results=[AnimalSearchResponse(likes=likes[r.id].count, **r.dict()) for r in results.results],
        )
        return searched
