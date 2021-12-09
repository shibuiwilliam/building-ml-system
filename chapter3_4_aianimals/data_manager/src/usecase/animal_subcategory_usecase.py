from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository
from src.request_object.animal_subcategory import AnimalSubcategoryCreateRequest, AnimalSubcategoryRequest
from src.response_object.animal_subcategory import AnimalSubcategoryResponse

logger = getLogger(__name__)


class AbstractAnimalSubcategoryUsecase(ABC):
    def __init__(
        self,
        animal_category_repository: AbstractAnimalCategoryRepository,
        animal_subcategory_repository: AbstractAnimalSubcategoryRepository,
    ):
        self.animal_category_repository = animal_category_repository
        self.animal_subcategory_repository = animal_subcategory_repository

    @abstractmethod
    def retrieve(
        self,
        session: Session,
        request: Optional[AnimalSubcategoryRequest] = None,
    ) -> List[AnimalSubcategoryResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        session: Session,
        request: AnimalSubcategoryCreateRequest,
    ) -> Optional[AnimalSubcategoryResponse]:
        raise NotImplementedError
