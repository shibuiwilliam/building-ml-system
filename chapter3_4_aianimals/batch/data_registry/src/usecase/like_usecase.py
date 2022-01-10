from abc import ABC, abstractmethod
from typing import List, Optional

from src.middleware.logger import configure_logger
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.like import LikeCreateRequest, LikeRequest
from src.response_object.like import LikeResponse

logger = configure_logger(__name__)


class AbstractLikeUsecase(ABC):
    def __init__(
        self,
        like_repository: AbstractLikeRepository,
    ):
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