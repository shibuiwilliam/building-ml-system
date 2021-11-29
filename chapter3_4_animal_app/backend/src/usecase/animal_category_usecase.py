from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.repository.animal_category_repository import AnimalCategoryRepository
from src.schema.animal_category import AnimalCategoryCreate, AnimalCategoryModel, AnimalCategoryQuery
from src.usecase.abstract_usecase import AbstractUsecase

logger = getLogger(__name__)


class AnimalCategoryUsecase(AbstractUsecase):
    def __init__(
        self,
        animal_category_repository: AnimalCategoryRepository,
    ):
        super().__init__()
        self.animal_category_repository = animal_category_repository

    def retrieve(
        self,
        session: Session,
        id: Optional[str] = None,
        name: Optional[str] = None,
        is_deleted: Optional[bool] = False,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalCategoryModel]:
        data = self.animal_category_repository.select(
            session=session,
            query=AnimalCategoryQuery(
                id=id,
                name=name,
                is_deleted=is_deleted,
            ),
            limit=limit,
            offset=offset,
        )
        return data

    def register(
        self,
        session: Session,
        record: AnimalCategoryCreate,
    ) -> Optional[AnimalCategoryModel]:
        data = self.animal_category_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        return data
