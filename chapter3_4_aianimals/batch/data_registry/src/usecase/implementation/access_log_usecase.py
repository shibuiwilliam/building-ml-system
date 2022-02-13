from datetime import datetime
from typing import List

from src.entities.access_log import AccessLogCreate, Action
from src.middleware.logger import configure_logger
from src.repository.access_log_repository import AbstractAccessLogRepository
from src.request_object.access_log import AccessLogCreateRequest
from src.usecase.access_log_usecase import AbstractAccessLogUsecase

logger = configure_logger(__name__)


class AccessLogUsecase(AbstractAccessLogUsecase):
    def __init__(
        self,
        access_log_repository: AbstractAccessLogRepository,
    ):
        super().__init__(access_log_repository=access_log_repository)

    def register(
        self,
        request: AccessLogCreateRequest,
    ):
        action = Action.value_to_key(value=request.action)
        if action is None:
            logger.error(f"invalid action: {request.action}")
            return
        record = AccessLogCreate(
            id=request.id,
            phrases=request.phrases,
            animal_category_id=request.animal_category_id,
            animal_subcategory_id=request.animal_subcategory_id,
            user_id=request.user_id,
            likes=request.likes,
            animal_id=request.animal_id,
            action=request.action,
            created_at=request.created_at,
        )
        self.access_log_repository.insert(
            record=record,
            commit=True,
        )

    def bulk_register(
        self,
        requests: List[AccessLogCreateRequest],
    ):
        records = [
            AccessLogCreate(
                id=request.id,
                phrases=request.phrases,
                animal_category_id=request.animal_category_id,
                animal_subcategory_id=request.animal_subcategory_id,
                user_id=request.user_id,
                likes=request.likes,
                animal_id=request.animal_id,
                action=request.action,
                created_at=request.created_at,
                updated_at=datetime.now(),
            )
            for request in requests
        ]
        for i in range(0, len(records), 200):
            self.access_log_repository.bulk_insert(
                records=records[i : i + 200],
                commit=True,
            )
            logger.info(f"bulk register access log: {i} to {i+200}")
