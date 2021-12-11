import json

from sqlalchemy.orm import Session
from src.controller.animal_subcategory_controller import AbstractAnimalSubcategoryController
from src.middleware.logger import configure_logger
from src.request_object.animal_subcategory import AnimalSubcategoryCreateRequest
from src.usecase.animal_subcategory_usecase import AbstractAnimalSubcategoryUsecase

logger = configure_logger(__name__)


class AnimalSubcategoryController(AbstractAnimalSubcategoryController):
    def __init__(
        self,
        animal_subcategory_usecase: AbstractAnimalSubcategoryUsecase,
    ):
        super().__init__(animal_subcategory_usecase=animal_subcategory_usecase)

    def register(
        self,
        session: Session,
        file_path: str,
    ):
        logger.info(f"register animal subcategory: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
        for k, v in data.items():
            logger.info(f"animal subcategory {k} {v}")
            request = AnimalSubcategoryCreateRequest(
                id=v["subcategory"],
                animal_category_id=v["category"],
                name_en=v["name_en"],
                name_ja=v["name_ja"],
            )
            self.animal_subcategory_usecase.register(
                session=session,
                request=request,
            )
        logger.info(f"done register animal subcategory: {file_path}")
