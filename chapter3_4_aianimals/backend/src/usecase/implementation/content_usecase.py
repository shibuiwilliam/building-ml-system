from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.content import ContentCreate, ContentQuery
from src.infrastructure.storage import AbstractStorage
from src.middleware.strings import get_uuid
from src.repository.content_repository import AbstractContentRepository
from src.repository.like_repository import AbstractLikeRepository
from src.repository.user_repository import AbstractUserRepository
from src.request_object.content import ContentCreateRequest, ContentRequest
from src.response_object.content import ContentResponse, ContentResponseWithLike
from src.response_object.user import UserResponse
from src.usecase.content_usecase import AbstractContentUsecase

logger = getLogger(__name__)


class ContentUsecase(AbstractContentUsecase):
    def __init__(
        self,
        like_repository: AbstractLikeRepository,
        user_repository: AbstractUserRepository,
        content_repository: AbstractContentRepository,
        storage_client: AbstractStorage,
    ):
        super().__init__(
            like_repository=like_repository,
            user_repository=user_repository,
            content_repository=content_repository,
            storage_client=storage_client,
        )

    def retrieve(
        self,
        session: Session,
        request: Optional[ContentRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ContentResponseWithLike]:
        if limit > 200:
            raise ValueError
        query: Optional[ContentQuery] = None
        if request is not None:
            query = ContentQuery(**request.dict())
        data = self.content_repository.select_with_like(
            session=session,
            query=query,
            limit=limit,
            offset=offset,
        )
        response = [ContentResponseWithLike(**d.dict()) for d in data]
        return response

    def liked_by(
        self,
        session: Session,
        content_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[UserResponse]:
        if limit > 200:
            raise ValueError
        data = self.content_repository.liked_by(
            session=session,
            content_id=content_id,
            limit=limit,
            offset=offset,
        )
        response = [UserResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        session: Session,
        request: ContentCreateRequest,
        local_file_path: str,
    ) -> Optional[ContentResponse]:
        id = get_uuid()
        photo_url = self.storage_client.upload_image(
            uuid=id,
            source_file_path=local_file_path,
        )
        logger.info(f"uploaded image to {photo_url}")
        record = ContentCreate(
            id=id,
            user_id=request.user_id,
            name=request.name,
            description=request.description,
            photo_url=photo_url,
        )
        data = self.content_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        if data is not None:
            response = ContentResponse(**data.dict())
            return response
        return None
