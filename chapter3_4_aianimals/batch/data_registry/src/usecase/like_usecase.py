import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from src.entities.like import LikeCreate, LikeQuery
from src.middleware.strings import get_uuid
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.like import LikeCreateRequest, LikeRequest
from src.response_object.like import LikeResponse


class AbstractLikeUsecase(ABC):
    def __init__(
        self,
        like_repository: AbstractLikeRepository,
    ):
        self.logger = logging.getLogger(__name__)
        self.like_repository = like_repository

    @abstractmethod
    def retrieve(
        self,
        request: Optional[LikeRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[LikeResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        request: LikeCreateRequest,
    ) -> Optional[LikeResponse]:
        raise NotImplementedError

    @abstractmethod
    def bulk_register(
        self,
        requests: List[LikeCreateRequest],
    ):
        raise NotImplementedError


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
        query: Optional[LikeQuery] = None
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
        self.logger.info(f"register: {request}")
        exists = self.like_repository.select(
            query=LikeQuery(
                animal_id=request.animal_id,
                user_id=request.user_id,
            ),
        )
        if len(exists) > 0:
            response = LikeResponse(**exists[0].dict())
            self.logger.info(f"exists: {response}")
            return response

        data = self.like_repository.insert(
            record=LikeCreate(
                id=get_uuid(),
                animal_id=request.animal_id,
                user_id=request.user_id,
            ),
            commit=True,
        )
        self.logger.info(f"registered: {data}")
        if data is not None:
            response = LikeResponse(**data.dict())
            self.logger.info(f"done register: {response}")
            return response
        return None

    def bulk_register(
        self,
        requests: List[LikeCreateRequest],
    ):
        records = [
            LikeCreate(
                id=request.id,
                animal_id=request.animal_id,
                user_id=request.user_id,
                created_at=request.created_at,
            )
            for request in requests
        ]
        for i in range(0, len(records), 200):
            _records = records[i : i + 200]
            self.like_repository.bulk_insert(
                records=_records,
                commit=True,
            )
            self.logger.info(f"bulk register like: {i} to {i+200}")
