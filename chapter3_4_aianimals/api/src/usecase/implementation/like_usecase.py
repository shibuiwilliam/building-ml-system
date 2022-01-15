from logging import getLogger
from typing import List, Optional

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from src.configurations import Configurations
from src.entities.like import LikeCreate, LikeDelete
from src.infrastructure.queue import AbstractQueue
from src.middleware.strings import get_uuid
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.like import LikeCreateRequest, LikeDeleteRequest, LikeRequest
from src.response_object.like import LikeResponse
from src.usecase.like_usecase import AbstractLikeUsecase

logger = getLogger(__name__)


class LikeUsecase(AbstractLikeUsecase):
    def __init__(
        self,
        like_repository: AbstractLikeRepository,
        queue: AbstractQueue,
    ):
        super().__init__(
            like_repository=like_repository,
            queue=queue,
        )

    def retrieve(
        self,
        session: Session,
        request: Optional[LikeRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[LikeResponse]:
        if limit > 200:
            raise ValueError
        query: Optional[LikeRequest] = None
        if request is not None:
            query = LikeRequest(**request.dict())
        data = self.like_repository.select(
            session=session,
            query=query,
            limit=limit,
            offset=offset,
        )
        response = [LikeResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        session: Session,
        request: LikeCreateRequest,
        background_tasks: BackgroundTasks,
    ) -> Optional[LikeResponse]:
        query = LikeRequest(
            animal_id=request.animal_id,
            user_id=request.user_id,
        )
        exist = self.like_repository.select(
            session=session,
            query=query,
            limit=1,
            offset=0,
        )
        logger.info(f"exist: {exist}")
        if len(exist) > 0:
            return None

        record = LikeCreate(
            id=get_uuid(),
            animal_id=request.animal_id,
            user_id=request.user_id,
        )
        logger.info(f"record: {record}")
        data = self.like_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        logger.info(f"registered: {data}")
        if data is not None:
            response = LikeResponse(**data.dict())
            background_tasks.add_task(
                self.queue.enqueue,
                Configurations.animal_registry_queue,
                data.animal_id,
            )
            return response
        return None

    def delete(
        self,
        session: Session,
        request: LikeDeleteRequest,
    ):
        record = LikeDelete(**request.dict())
        self.like_repository.delete(
            session=session,
            record=record,
            commit=True,
        )
