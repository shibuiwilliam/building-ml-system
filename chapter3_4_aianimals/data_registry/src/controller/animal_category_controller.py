from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from src.middleware.logger import configure_logger
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase

logger = configure_logger(__name__)


class AbstractAnimalCategoryController(ABC):
    def __init__(
        self,
        animal_category_usecase: AbstractAnimalCategoryUsecase,
    ):
        self.animal_category_usecase = animal_category_usecase

    @abstractmethod
    def register(
        self,
        session: Session,
        file_path: str,
    ):
        raise NotImplementedError
