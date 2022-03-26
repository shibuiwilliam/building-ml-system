from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.animal_category import AnimalCategoryCreate, AnimalCategoryQuery
from src.middleware.strings import get_uuid
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.request_object.animal_category import AnimalCategoryCreateRequest, AnimalCategoryRequest
from src.response_object.animal_category import AnimalCategoryResponse

logger = getLogger(__name__)


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
        record = AnimalCategoryCreate(
            id=get_uuid(),
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
            return response
        return None
