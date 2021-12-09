from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session
from src.middleware.logger import configure_logger
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.request_object.animal_category import AnimalCategoryCreateRequest, AnimalCategoryRequest
from src.response_object.animal_category import AnimalCategoryResponse

logger = configure_logger(__name__)


class AbstractAnimalCategoryUsecase(ABC):
    def __init__(
        self,
        animal_category_repository: AbstractAnimalCategoryRepository,
    ):
        self.animal_category_repository = animal_category_repository

    @abstractmethod
    def retrieve(
        self,
        session: Session,
        request: Optional[AnimalCategoryRequest] = None,
    ) -> List[AnimalCategoryResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        session: Session,
        request: AnimalCategoryCreateRequest,
    ) -> Optional[AnimalCategoryResponse]:
        raise NotImplementedError
