import json

from sqlalchemy.orm import Session
from src.controller.animal_category_controller import AbstractAnimalCategoryController
from src.middleware.logger import configure_logger
from src.request_object.animal_category import AnimalCategoryCreateRequest
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase

logger = configure_logger(__name__)


class AnimalCategoryController(AbstractAnimalCategoryController):
    def __init__(
        self,
        animal_category_usecase: AbstractAnimalCategoryUsecase,
    ):
        super().__init__(animal_category_usecase=animal_category_usecase)

    def register(
        self,
        session: Session,
        file_path: str,
    ):
        logger.info(f"register animal category: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
        for k, v in data.items():
            logger.info(f"animal category {k} {v}")
            request = AnimalCategoryCreateRequest(
                id=v["category"],
                name_en=v["name_en"],
                name_ja=v["name_ja"],
            )
            self.animal_category_usecase.register(
                session=session,
                request=request,
            )
        logger.info(f"done register animal category: {file_path}")
