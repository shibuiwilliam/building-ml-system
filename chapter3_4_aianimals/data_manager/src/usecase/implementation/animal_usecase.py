from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.animal import AnimalCreate, AnimalQuery
from src.middleware.logger import configure_logger
from src.middleware.strings import get_uuid
from src.repository.animal_repository import AbstractAnimalRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest
from src.response_object.animal import AnimalResponse, AnimalResponseWithLike
from src.usecase.animal_usecase import AbstractAnimalUsecase

logger = configure_logger(__name__)


class AnimalUsecase(AbstractAnimalUsecase):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
    ):
        super().__init__(animal_repository=animal_repository)

    def retrieve(
        self,
        session: Session,
        request: Optional[AnimalRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AnimalResponseWithLike]:
        if limit > 200:
            raise ValueError
        query: Optional[AnimalQuery] = None
        if request is not None:
            query = AnimalQuery(**request.dict())
        data = self.animal_repository.select(
            session=session,
            query=query,
            limit=limit,
            offset=offset,
        )
        response = [AnimalResponseWithLike(**d.dict()) for d in data]
        return response

    def register(
        self,
        session: Session,
        request: AnimalCreateRequest,
    ) -> Optional[AnimalResponse]:
        id = get_uuid()
        record = AnimalCreate(
            id=id,
            animal_category_id=request.animal_category_id,
            animal_subcategory_id=request.animal_subcategory_id,
            user_id=request.user_id,
            name=request.name,
            description=request.description,
            photo_url=request.photo_url,
        )
        data = self.animal_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        if data is not None:
            response = AnimalResponse(**data.dict())
            return response
        return None
