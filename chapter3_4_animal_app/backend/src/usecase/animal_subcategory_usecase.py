from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.repository.animal_category_repository import AnimalCategoryRepository
from src.repository.animal_subcategory_repository import AnimalSubcategoryRepository
from src.schema.animal_category import AnimalCategoryQuery
from src.schema.animal_subcategory import AnimalSubcategoryCreate, AnimalSubcategoryModel, AnimalSubcategoryQuery
from src.usecase.abstract_usecase import AbstractUsecase

logger = getLogger(__name__)


class AnimalSubcategoryUsecase(AbstractUsecase):
    def __init__(
        self,
        animal_subcategory_repository: AnimalSubcategoryRepository,
        animal_category_repository: AnimalCategoryRepository,
    ):
        super().__init__()
        self.animal_subcategory_repository = animal_subcategory_repository
        self.animal_category_repository = animal_category_repository

    def retrieve(
        self,
        session: Session,
        id: Optional[str],
        name: Optional[str] = None,
        animal_category_name: Optional[str] = None,
        is_deleted: Optional[bool] = False,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalSubcategoryModel]:
        animal_category_id: Optional[str] = None
        if animal_category_name is not None:
            animal_category = self.animal_category_repository.select(
                session=session,
                query=AnimalCategoryQuery(name=animal_category_name),
                limit=1,
                offset=0,
            )
            animal_category_id = animal_category[0].id

        data = self.animal_subcategory_repository.select(
            session=session,
            query=AnimalSubcategoryQuery(
                id=id,
                animal_category_id=animal_category_id,
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
        record: AnimalSubcategoryCreate,
    ) -> Optional[AnimalSubcategoryModel]:
        data = self.animal_subcategory_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        return data
