from abc import ABC, abstractmethod
from logging import getLogger

from sqlalchemy.orm import Session
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository
from src.response_object.metadata import MetadataResponse

logger = getLogger(__name__)


class AbstractMetadataUsecase(ABC):
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
    ) -> MetadataResponse:
        raise NotImplementedError
