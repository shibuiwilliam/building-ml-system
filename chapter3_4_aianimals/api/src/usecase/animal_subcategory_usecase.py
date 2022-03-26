from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.animal_category import AnimalCategoryQuery
from src.entities.animal_subcategory import AnimalSubcategoryCreate, AnimalSubcategoryQuery
from src.middleware.strings import get_uuid
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


class AnimalSubcategoryUsecase(AbstractAnimalSubcategoryUsecase):
    def __init__(
        self,
        animal_category_repository: AbstractAnimalCategoryRepository,
        animal_subcategory_repository: AbstractAnimalSubcategoryRepository,
    ):
        super().__init__(
            animal_subcategory_repository=animal_subcategory_repository,
            animal_category_repository=animal_category_repository,
        )

    def retrieve(
        self,
        session: Session,
        request: Optional[AnimalSubcategoryRequest] = None,
    ) -> List[AnimalSubcategoryResponse]:
        animal_category_id: Optional[int] = None
        if request is not None:
            _query = AnimalCategoryQuery()
            if request.animal_category_name_en is not None:
                _query.name_en = request.animal_category_name_en
            if request.animal_category_name_ja is not None:
                _query.name_ja = request.animal_category_name_ja
            if _query.name_en is not None or _query.name_ja is not None:
                animal_category = self.animal_category_repository.select(
                    session=session,
                    query=_query,
                )
                animal_category_id = animal_category[0].id

        query: Optional[AnimalSubcategoryQuery] = None
        if request is not None:
            query = AnimalSubcategoryQuery(
                id=request.id,
                animal_category_id=animal_category_id,
                name_en=request.name_en,
                name_ja=request.name_ja,
                is_deleted=request.is_deleted,
            )

        data = self.animal_subcategory_repository.select(
            session=session,
            query=query,
        )
        response = [AnimalSubcategoryResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        session: Session,
        request: AnimalSubcategoryCreateRequest,
    ) -> Optional[AnimalSubcategoryResponse]:
        record = AnimalSubcategoryCreate(
            id=get_uuid(),
            animal_category_id=request.animal_category_id,
            name_en=request.name_en,
            name_ja=request.name_ja,
        )
        data = self.animal_subcategory_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        if data is not None:
            response = AnimalSubcategoryResponse(**data.dict())
            return response
        return None
