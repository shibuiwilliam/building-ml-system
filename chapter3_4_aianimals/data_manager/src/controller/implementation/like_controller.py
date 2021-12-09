import json

from sqlalchemy.orm import Session
from src.controller.like_controller import AbstractLikeController
from src.middleware.logger import configure_logger
from src.request_object.like import LikeCreateRequest
from src.usecase.like_usecase import AbstractLikeUsecase

logger = configure_logger(__name__)


class LikeController(AbstractLikeController):
    def __init__(
        self,
        like_usecase: AbstractLikeUsecase,
    ):
        super().__init__(like_usecase=like_usecase)

    def register(
        self,
        session: Session,
        file_path: str,
    ):
        with open(file_path, "r") as f:
            data = json.load(f)
        for _, v in data.items():
            request = LikeCreateRequest(
                animal_id=v["animal_id"],
                user_id=v["user_id"],
            )
            self.like_usecase.register(
                session=session,
                request=request,
            )
