from logging import getLogger

from sqlalchemy.orm import Session
from src.entities.animal_category import AnimalCategoryQuery
from src.entities.animal_subcategory import AnimalSubcategoryQuery
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository
from src.response_object.metadata import MetadataResponse
from src.usecase.metadata_usecase import AbstractMetadataUsecase

logger = getLogger(__name__)


class MetadataUsecase(AbstractMetadataUsecase):
    def __init__(
        self,
        animal_category_repository: AbstractAnimalCategoryRepository,
        animal_subcategory_repository: AbstractAnimalSubcategoryRepository,
    ):
        super().__init__(
            animal_category_repository=animal_category_repository,
            animal_subcategory_repository=animal_subcategory_repository,
        )
        pass

    def retrieve(
        self,
        session: Session,
    ) -> MetadataResponse:
        animal_category = self.animal_category_repository.select(
            session=session,
            query=AnimalCategoryQuery(
                is_deleted=False,
            ),
        )
        animal_subcategory = self.animal_subcategory_repository.select(
            session=session,
            query=AnimalSubcategoryQuery(
                is_deleted=False,
            ),
        )
        response = MetadataResponse(
            animal_category=animal_category,
            animal_subcategory=animal_subcategory,
        )
        return response
