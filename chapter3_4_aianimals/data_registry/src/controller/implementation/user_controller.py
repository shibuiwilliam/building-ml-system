import json
from datetime import datetime

from sqlalchemy.orm import Session
from src.controller.user_controller import AbstractUserController
from src.middleware.logger import configure_logger
from src.request_object.user import UserCreateRequest
from src.usecase.user_usecase import AbstractUserUsecase

logger = configure_logger(__name__)


class UserController(AbstractUserController):
    def __init__(
        self,
        user_usecase: AbstractUserUsecase,
    ):
        super().__init__(user_usecase=user_usecase)

    def register(
        self,
        session: Session,
        file_path: str,
    ):
        logger.info(f"register user: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
        for k, v in data.items():
            request = UserCreateRequest(
                id=k,
                handle_name=v["handle_name"],
                email_address=v["email_address"],
                password=v["password"],
                age=v["age"],
                gender=v["gender"],
                created_at=datetime.strptime(v["created_at"], "%Y-%m-%dT%H:%M:%S.%f"),
            )
            self.user_usecase.register(
                session=session,
                request=request,
            )
        logger.info(f"done register user: {file_path}")
