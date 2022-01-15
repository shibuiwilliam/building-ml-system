from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from src.infrastructure.queue import AbstractQueue
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.like import LikeCreateRequest, LikeDeleteRequest, LikeRequest
from src.response_object.like import LikeResponse

logger = getLogger(__name__)


class AbstractLikeUsecase(ABC):
    def __init__(
        self,
        like_repository: AbstractLikeRepository,
        queue: AbstractQueue,
    ):
        self.like_repository = like_repository
        self.queue = queue

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
        background_tasks: BackgroundTasks,
    ) -> Optional[LikeResponse]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        session: Session,
        request: LikeDeleteRequest,
    ):
        raise NotImplementedError
