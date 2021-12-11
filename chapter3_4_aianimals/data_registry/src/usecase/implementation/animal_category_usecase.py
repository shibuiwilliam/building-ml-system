from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.animal_category import AnimalCategoryCreate, AnimalCategoryQuery
from src.middleware.logger import configure_logger
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.request_object.animal_category import AnimalCategoryCreateRequest, AnimalCategoryRequest
from src.response_object.animal_category import AnimalCategoryResponse
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase

logger = configure_logger(__name__)


class AnimalCategoryUsecase(AbstractAnimalCategoryUsecase):
    def __init__(
        self,
        animal_category_repository: AbstractAnimalCategoryRepository,
    ):
        super().__init__(animal_category_repository=animal_category_repository)

    def retrieve(
        self,
        session: Session,
        request: Optional[AnimalCategoryRequest] = None,
    ) -> List[AnimalCategoryResponse]:
        query: Optional[AnimalCategoryQuery] = None
        if request is not None:
            query = AnimalCategoryQuery(**request.dict())

        data = self.animal_category_repository.select(
            session=session,
            query=query,
        )
        response = [AnimalCategoryResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        session: Session,
        request: AnimalCategoryCreateRequest,
    ) -> Optional[AnimalCategoryResponse]:
        logger.info(f"register: {request}")
        exists = self.animal_category_repository.select(
            session=session,
            query=AnimalCategoryQuery(id=request.id),
        )
        if len(exists) > 0:
            response = AnimalCategoryResponse(**exists[0].dict())
            logger.info(f"exists: {response}")
            return response

        record = AnimalCategoryCreate(
            id=request.id,
            name_en=request.name_en,
            name_ja=request.name_ja,
        )
        data = self.animal_category_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        if data is not None:
            response = AnimalCategoryResponse(**data.dict())
            logger.info(f"done register: {response}")
            return response
        return None
