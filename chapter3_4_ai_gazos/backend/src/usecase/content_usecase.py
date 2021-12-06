from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.infrastructure.storage import AbstractStorage
from src.repository.content_repository import AbstractContentRepository
from src.repository.like_repository import AbstractLikeRepository
from src.repository.user_repository import AbstractUserRepository
from src.request_object.content import ContentCreateRequest, ContentRequest
from src.response_object.content import ContentResponse, ContentResponseWithLike
from src.response_object.user import UserResponse

logger = getLogger(__name__)


class AbstractContentUsecase(ABC):
    def __init__(
        self,
        like_repository: AbstractLikeRepository,
        user_repository: AbstractUserRepository,
        content_repository: AbstractContentRepository,
        storage_client: AbstractStorage,
    ):
        self.like_repository = like_repository
        self.user_repository = user_repository
        self.content_repository = content_repository
        self.storage_client = storage_client

    @abstractmethod
    def retrieve(
        self,
        session: Session,
        request: Optional[ContentRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ContentResponseWithLike]:
        raise NotImplementedError

    @abstractmethod
    def liked_by(
        self,
        session: Session,
        content_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[UserResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        session: Session,
        request: ContentCreateRequest,
        local_file_path: str,
    ) -> Optional[ContentResponse]:
        raise NotImplementedError
