from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.animal import AnimalQuery
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository
from src.repository.like_repository import AbstractLikeRepository
from src.repository.user_repository import AbstractUserRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest
from src.response_object.animal import AnimalResponse, AnimalResponseWithLike
from src.response_object.user import UserResponse
from src.usecase.animal_usecase import AbstractAnimalUsecase

logger = getLogger(__name__)


class AnimalUsecase(AbstractAnimalUsecase):
    def __init__(
        self,
        like_repository: AbstractLikeRepository,
        user_repository: AbstractUserRepository,
        animal_category_repository: AbstractAnimalCategoryRepository,
        animal_subcategory_repository: AbstractAnimalSubcategoryRepository,
        animal_repository: AbstractAnimalRepository,
    ):
        super().__init__(
            like_repository=like_repository,
            user_repository=user_repository,
            animal_repository=animal_repository,
            animal_subcategory_repository=animal_subcategory_repository,
            animal_category_repository=animal_category_repository,
        )

    def retrieve(
        self,
        session: Session,
        request: Optional[AnimalRequest] = None,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalResponseWithLike]:
        if limit is None:
            limit = 100
        if offset is None:
            offset = 0
        if limit > 200:
            raise ValueError("limit cannot be more than 200")
        query: Optional[AnimalQuery] = None
        if request is not None:
            query = AnimalQuery(**request.dict())
        data = self.animal_repository.select_with_like(
            session=session,
            query=query,
            limit=limit,
            offset=offset,
        )
        response = [AnimalResponseWithLike(**d.dict()) for d in data]
        return response

    def liked_by(
        self,
        session: Session,
        animal_id: str,
    ) -> List[UserResponse]:
        data = self.animal_repository.liked_by(
            session=session,
            animal_id=animal_id,
        )
        response = [UserResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        session: Session,
        record: AnimalCreateRequest,
    ) -> Optional[AnimalResponse]:
        data = self.animal_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        if data is not None:
            response = AnimalResponse(**data.dict())
            return response
        return None
