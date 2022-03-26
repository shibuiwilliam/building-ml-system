from abc import ABC, abstractmethod
from logging import getLogger

from sqlalchemy.orm import Session
from src.entities.access_log import AccessLogCreate, Action
from src.middleware.strings import get_uuid
from src.repository.access_log_repository import AbstractAccessLogRepository
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.access_log import AccessLogCreateRequest

logger = getLogger(__name__)


class AbstractAccessLogUsecase(ABC):
    def __init__(
        self,
        access_log_repository: AbstractAccessLogRepository,
        like_repository: AbstractLikeRepository,
    ):
        self.access_log_repository = access_log_repository
        self.like_repository = like_repository

    @abstractmethod
    def register(
        self,
        session: Session,
        request: AccessLogCreateRequest,
    ):
        raise NotImplementedError


class AccessLogUsecase(AbstractAccessLogUsecase):
    def __init__(
        self,
        access_log_repository: AbstractAccessLogRepository,
        like_repository: AbstractLikeRepository,
    ):
        super().__init__(
            access_log_repository=access_log_repository,
            like_repository=like_repository,
        )

    def register(
        self,
        session: Session,
        request: AccessLogCreateRequest,
    ):
        action = Action.value_to_key(value=request.action)
        if action is None:
            logger.error(f"invalid action: {request.action}")
            return
        likes = self.like_repository.count(
            session=session,
            animal_ids=[request.animal_id],
        )
        like_count = likes[request.animal_id].count

        record = AccessLogCreate(
            id=get_uuid(),
            phrases=request.phrases,
            animal_category_id=request.animal_category_id,
            animal_subcategory_id=request.animal_subcategory_id,
            user_id=request.user_id,
            likes=like_count,
            animal_id=request.animal_id,
            action=action,
            created_at=request.created_at,
        )
        self.access_log_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
