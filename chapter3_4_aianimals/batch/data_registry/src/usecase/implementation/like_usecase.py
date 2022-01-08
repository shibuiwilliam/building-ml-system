from typing import List, Optional

from src.entities.like import LikeCreate, LikeQuery
from src.middleware.logger import configure_logger
from src.middleware.strings import get_uuid
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.like import LikeCreateRequest, LikeRequest
from src.response_object.like import LikeResponse
from src.usecase.like_usecase import AbstractLikeUsecase

logger = configure_logger(__name__)


class LikeUsecase(AbstractLikeUsecase):
    def __init__(
        self,
        like_repository: AbstractLikeRepository,
    ):
        super().__init__(like_repository=like_repository)

    def retrieve(
        self,
        request: Optional[LikeRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[LikeResponse]:
        if limit > 200:
            raise ValueError
        query: Optional[LikeRequest] = None
        if request is not None:
            query = LikeQuery(**request.dict())
        data = self.like_repository.select(
            query=query,
            limit=limit,
            offset=offset,
        )
        response = [LikeResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        request: LikeCreateRequest,
    ) -> Optional[LikeResponse]:
        logger.info(f"register: {request}")
        exists = self.like_repository.select(
            query=LikeQuery(
                animal_id=request.animal_id,
                user_id=request.user_id,
            ),
        )
        if len(exists) > 0:
            response = LikeResponse(**exists[0].dict())
            logger.info(f"exists: {response}")
            return response

        record = LikeCreate(
            id=get_uuid(),
            animal_id=request.animal_id,
            user_id=request.user_id,
        )
        data = self.like_repository.insert(
            record=record,
            commit=True,
        )
        logger.info(f"registered: {data}")
        if data is not None:
            response = LikeResponse(**data.dict())
            logger.info(f"done register: {response}")
            return response
        return None
