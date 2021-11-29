from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.repository.animal_category_repository import AnimalCategoryRepository
from src.repository.animal_repository import AnimalRepository
from src.repository.animal_subcategory_repository import AnimalSubcategoryRepository
from src.schema.animal import AnimalCreate, AnimalModel, AnimalQuery
from src.schema.animal_category import AnimalCategoryQuery
from src.schema.animal_subcategory import AnimalSubcategoryQuery
from src.usecase.abstract_usecase import AbstractUsecase

logger = getLogger(__name__)


class AnimalUsecase(AbstractUsecase):
    def __init__(
        self,
        animal_repository: AnimalRepository,
        animal_subcategory_repository: AnimalSubcategoryRepository,
        animal_category_repository: AnimalCategoryRepository,
    ):
        super().__init__()
        self.animal_repository = animal_repository
        self.animal_subcategory_repository = animal_subcategory_repository
        self.animal_category_repository = animal_category_repository

    def retrieve(
        self,
        session: Session,
        id: Optional[str] = None,
        name: Optional[str] = None,
        animal_category_name: Optional[str] = None,
        animal_subcategory_name: Optional[str] = None,
        user_id: Optional[str] = None,
        deactivated: Optional[bool] = False,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalModel]:
        animal_category_id: Optional[str] = None
        if animal_category_name is not None:
            animal_category = self.animal_category_repository.select(
                session=session,
                query=AnimalCategoryQuery(name=animal_category_name),
                limit=1,
                offset=0,
            )
            animal_category_id = animal_category[0].id

        animal_subcategory_id: Optional[str] = None
        if animal_subcategory_name is not None:
            animal_subcategory = self.animal_subcategory_repository.select(
                session=session,
                query=AnimalSubcategoryQuery(name=animal_subcategory_name),
                limit=1,
                offset=0,
            )
            animal_subcategory_id = animal_subcategory[0].id

        data = self.animal_repository.select(
            session=session,
            query=AnimalQuery(
                id=id,
                name=name,
                animal_category_id=animal_category_id,
                animal_subcategory_id=animal_subcategory_id,
                user_id=user_id,
                deactivated=deactivated,
            ),
            limit=limit,
            offset=offset,
        )
        return data

    def register(
        self,
        session: Session,
        record: AnimalCreate,
    ) -> Optional[AnimalModel]:
        data = self.animal_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        return data
