import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from src.entities.animal_category import AnimalCategoryCreate, AnimalCategoryQuery
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.request_object.animal_category import AnimalCategoryCreateRequest, AnimalCategoryRequest
from src.response_object.animal_category import AnimalCategoryResponse


class AbstractAnimalCategoryUsecase(ABC):
    def __init__(
        self,
        animal_category_repository: AbstractAnimalCategoryRepository,
    ):
        self.logger = logging.getLogger(__name__)
        self.animal_category_repository = animal_category_repository

    @abstractmethod
    def retrieve(
        self,
        request: Optional[AnimalCategoryRequest] = None,
    ) -> List[AnimalCategoryResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        request: AnimalCategoryCreateRequest,
    ) -> Optional[AnimalCategoryResponse]:
        raise NotImplementedError


class AnimalCategoryUsecase(AbstractAnimalCategoryUsecase):
    def __init__(
        self,
        animal_category_repository: AbstractAnimalCategoryRepository,
    ):
        super().__init__(animal_category_repository=animal_category_repository)

    def retrieve(
        self,
        request: Optional[AnimalCategoryRequest] = None,
    ) -> List[AnimalCategoryResponse]:
        query: Optional[AnimalCategoryQuery] = None
        if request is not None:
            query = AnimalCategoryQuery(**request.dict())

        data = self.animal_category_repository.select(
            query=query,
        )
        response = [AnimalCategoryResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        request: AnimalCategoryCreateRequest,
    ) -> Optional[AnimalCategoryResponse]:
        self.logger.info(f"register: {request}")
        exists = self.animal_category_repository.select(
            query=AnimalCategoryQuery(id=request.id),
        )
        if len(exists) > 0:
            response = AnimalCategoryResponse(**exists[0].dict())
            self.logger.info(f"exists: {response}")
            return response

        data = self.animal_category_repository.insert(
            record=AnimalCategoryCreate(
                id=request.id,
                name_en=request.name_en,
                name_ja=request.name_ja,
            ),
            commit=True,
        )
        if data is not None:
            response = AnimalCategoryResponse(**data.dict())
            self.logger.info(f"done register: {response}")
            return response
        return None
