import json
from datetime import datetime

from sqlalchemy.orm import Session
from src.controller.animal_controller import AbstractAnimalController
from src.middleware.logger import configure_logger
from src.request_object.animal import AnimalCreateRequest
from src.usecase.animal_usecase import AbstractAnimalUsecase

logger = configure_logger(__name__)


class AnimalController(AbstractAnimalController):
    def __init__(
        self,
        animal_usecase: AbstractAnimalUsecase,
    ):
        super().__init__(animal_usecase=animal_usecase)

    def register(
        self,
        session: Session,
        file_path: str,
    ):
        with open(file_path, "r") as f:
            data = json.load(f)
        for k, v in data.items():
            request = AnimalCreateRequest(
                id=k,
                animal_category_id=v["category"],
                animal_subcategory_id=v["subcategory"],
                user_id=v["user_id"],
                photo_url=v["photo_url"],
                name=v["filename"],
                description="",
                created_at=datetime.strptime(v["created_at"], "%Y-%m-%dT%H:%M:%S.%f"),
            )
            self.animal_usecase.register(
                session=session,
                request=request,
            )
