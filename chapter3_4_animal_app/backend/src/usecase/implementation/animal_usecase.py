from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.repository.animal_category_repository import AnimalCategoryRepository
from src.repository.animal_repository import AnimalRepository
from src.repository.animal_subcategory_repository import AnimalSubcategoryRepository
from src.repository.like_repository import LikeRepository
from src.schema.animal import AnimalCreate, AnimalModel, AnimalModelWithLike, AnimalQuery
from src.schema.animal_category import AnimalCategoryQuery
from src.schema.animal_subcategory import AnimalSubcategoryQuery
from src.schema.like import LikeQuery
from src.schema.schema import Count
from src.schema.user import UserModel
from src.usecase.abstract_usecase import AbstractUsecase

logger = getLogger(__name__)


class AnimalUsecase(AbstractUsecase):
    def __init__(
        self,
        animal_repository: AnimalRepository,
        animal_subcategory_repository: AnimalSubcategoryRepository,
        animal_category_repository: AnimalCategoryRepository,
        like_repository: LikeRepository,
    ):
        super().__init__()
        self.animal_repository = animal_repository
        self.animal_subcategory_repository = animal_subcategory_repository
        self.animal_category_repository = animal_category_repository
        self.like_repository = like_repository

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
    ) -> List[AnimalModelWithLike]:
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
        animal_ids = [d.id for d in data]
        counts = self.like_repository.count(
            session=session,
            animal_ids=animal_ids,
        )
        animal_model_with_likes = []
        for d in data:
            animal_model_with_likes.append(
                AnimalModelWithLike(
                    id=d.id,
                    animal_category_id=d.animal_category_id,
                    animal_category_name=d.animal_category_name,
                    animal_subcategory_id=d.animal_subcategory_id,
                    animal_subcategory_name=d.animal_subcategory_name,
                    user_id=d.user_id,
                    user_handle_name=d.user_handle_name,
                    name=d.name,
                    description=d.description,
                    photo_url=d.photo_url,
                    like=counts.get(d.id, Count(count=0)).count,
                    deactivated=d.deactivated,
                    created_at=d.created_at,
                    updated_at=d.updated_at,
                )
            )
        return animal_model_with_likes

    def liked_by(
        self,
        session: Session,
        animal_id: str,
    ) -> List[UserModel]:
        limit = 100
        offset = 0
        likes = []
        while True:
            l = self.like_repository.select(
                session=session,
                query=LikeQuery(animal_id=animal_id),
                limit=limit,
                offset=offset,
            )
            if len(l) == 0:
                break
            likes.extend(l)
            offset += limit

        user_ids = [l.user_id for l in likes]
        limit = 100
        offset = 0
        users = []
        while True:
            u = self.user_repository.select_by_ids(
                session=session,
                user_ids=user_ids,
                limit=limit,
                offset=offset,
            )
            if len(u) == 0:
                break
            users.extend(u)
            offset += limit
        return users

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
