from logging import getLogger
from typing import Dict, List, Optional

from sqlalchemy.orm import Session
from src.repository.like_repository import LikeRepository
from src.schema.like import LikeCreate, LikeModel, LikeQuery
from src.schema.schema import Count
from src.usecase.abstract_usecase import AbstractUsecase

logger = getLogger(__name__)


class LikeUsecase(AbstractUsecase):
    def __init__(
        self,
        like_repository: LikeRepository,
    ):
        super().__init__()
        self.like_repository = like_repository

    def retrieve(
        self,
        session: Session,
        id: Optional[str] = None,
        animal_id: Optional[str] = None,
        user_id: Optional[str] = None,
        animal_name: Optional[str] = None,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[LikeModel]:
        data = self.like_repository.select(
            session=session,
            query=LikeQuery(
                id=id,
                animal_id=animal_id,
                user_id=user_id,
                animal_name=animal_name,
            ),
            limit=limit,
            offset=offset,
        )
        return data

    def count(
        self,
        session: Session,
        animal_ids: List[str],
    ) -> Dict[str, Count]:
        data = self.like_repository.count(
            session=session,
            animal_ids=animal_ids,
        )
        return data

    def register(
        self,
        session: Session,
        record: LikeCreate,
    ) -> Optional[LikeModel]:
        data = self.like_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        return data
