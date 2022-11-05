import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from src.entities.animal_subcategory import AnimalSubcategoryCreate, AnimalSubcategoryQuery
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository
from src.request_object.animal_subcategory import AnimalSubcategoryCreateRequest, AnimalSubcategoryRequest
from src.response_object.animal_subcategory import AnimalSubcategoryResponse


class AbstractAnimalSubcategoryUsecase(ABC):
    def __init__(
        self,
        animal_subcategory_repository: AbstractAnimalSubcategoryRepository,
    ):
        self.logger = logging.getLogger(__name__)
        self.animal_subcategory_repository = animal_subcategory_repository

    @abstractmethod
    def retrieve(
        self,
        request: Optional[AnimalSubcategoryRequest] = None,
    ) -> List[AnimalSubcategoryResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        request: AnimalSubcategoryCreateRequest,
    ) -> Optional[AnimalSubcategoryResponse]:
        raise NotImplementedError


class AnimalSubcategoryUsecase(AbstractAnimalSubcategoryUsecase):
    def __init__(
        self,
        animal_subcategory_repository: AbstractAnimalSubcategoryRepository,
    ):
        super().__init__(animal_subcategory_repository=animal_subcategory_repository)

    def retrieve(
        self,
        request: Optional[AnimalSubcategoryRequest] = None,
    ) -> List[AnimalSubcategoryResponse]:
        query: Optional[AnimalSubcategoryQuery] = None
        if request is not None:
            query = AnimalSubcategoryQuery(**request.dict())

        data = self.animal_subcategory_repository.select(
            query=query,
        )
        response = [AnimalSubcategoryResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        request: AnimalSubcategoryCreateRequest,
    ) -> Optional[AnimalSubcategoryResponse]:
        self.logger.info(f"register: {request}")
        exists = self.animal_subcategory_repository.select(
            query=AnimalSubcategoryQuery(id=request.id),
        )
        if len(exists) > 0:
            response = AnimalSubcategoryResponse(**exists[0].dict())
            self.logger.info(f"exists: {response}")
            return response

        data = self.animal_subcategory_repository.insert(
            record=AnimalSubcategoryCreate(
                id=request.id,
                animal_category_id=request.animal_category_id,
                name_en=request.name_en,
                name_ja=request.name_ja,
            ),
            commit=True,
        )
        if data is not None:
            response = AnimalSubcategoryResponse(**data.dict())
            self.logger.info(f"done register: {response}")
            return response
        return None
