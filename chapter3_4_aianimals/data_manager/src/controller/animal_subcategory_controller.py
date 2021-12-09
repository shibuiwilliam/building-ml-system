from abc import ABC, abstractmethod

from sqlalchemy.orm import Session
from src.middleware.logger import configure_logger
from src.usecase.animal_subcategory_usecase import AbstractAnimalSubcategoryUsecase

logger = configure_logger(__name__)


class AbstractAnimalSubcategoryController(ABC):
    def __init__(
        self,
        animal_subcategory_usecase: AbstractAnimalSubcategoryUsecase,
    ):
        self.animal_subcategory_usecase = animal_subcategory_usecase

    @abstractmethod
    def register(
        self,
        session: Session,
        file_path: str,
    ):
        raise NotImplementedError
