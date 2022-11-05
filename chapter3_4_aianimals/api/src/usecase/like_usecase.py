from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.like import LikeCreate, LikeDelete, LikeQuery
from src.infrastructure.cache import AbstractCache
from src.middleware.strings import get_uuid
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.like import LikeCreateRequest, LikeDeleteRequest, LikeRequest
from src.response_object.like import LikeResponse

logger = getLogger(__name__)


class AbstractLikeUsecase(ABC):
    def __init__(
        self,
        like_repository: AbstractLikeRepository,
        cache: AbstractCache,
    ):
        self.like_repository = like_repository
        self.cache = cache

    @abstractmethod
    def retrieve(
        self,
        session: Session,
        request: Optional[LikeRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[LikeResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        session: Session,
        request: LikeCreateRequest,
    ) -> Optional[LikeResponse]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        session: Session,
        request: LikeDeleteRequest,
    ):
        raise NotImplementedError


class LikeUsecase(AbstractLikeUsecase):
    def __init__(
        self,
        like_repository: AbstractLikeRepository,
        cache: AbstractCache,
    ):
        super().__init__(
            like_repository=like_repository,
            cache=cache,
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
        query: Optional[LikeQuery] = None
        if request is not None:
            query = LikeQuery(**request.dict())
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
    ) -> Optional[LikeResponse]:
        query = LikeQuery(
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
