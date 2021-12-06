from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, List, Optional

from sqlalchemy.orm import Session
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.like import LikeCreateRequest, LikeDeleteRequest, LikeRequest
from src.response_object.like import LikeResponse

logger = getLogger(__name__)


class AbstractLikeUsecase(ABC):
    def __init__(
        self,
        like_repository: AbstractLikeRepository,
    ):
        self.like_repository = like_repository

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
