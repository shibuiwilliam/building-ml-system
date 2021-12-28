from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.entities.like import LikeCreate, LikeModel, LikeQuery
from src.middleware.logger import configure_logger
from src.repository.like_repository import AbstractLikeRepository
from src.schema.like import Like
from src.schema.table import TABLES

logger = configure_logger(__name__)


class LikeRepository(AbstractLikeRepository):
    def __init__(self) -> None:
        super().__init__()
        self.table_name = TABLES.LIKE.value

    def select(
        self,
        session: Session,
        query: Optional[LikeQuery],
        limit: int = 100,
        offset: int = 0,
    ) -> List[LikeModel]:
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(Like.id == query.id)
            if query.animal_id is not None:
                filters.append(Like.animal_id == query.animal_id)
            if query.user_id is not None:
                filters.append(Like.user_id == query.user_id)
        results = session.query(Like).filter(and_(*filters)).order_by(Like.id).limit(limit).offset(offset)
        data = [
            LikeModel(
                id=d.id,
                animal_id=d.animal_id,
                user_id=d.user_id,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in results
        ]
        return data

    def insert(
        self,
        session: Session,
        record: LikeCreate,
        commit: bool = True,
    ) -> Optional[LikeModel]:
        data = Like(**record.dict())
        session.add(data)
        if commit:
            session.commit()
            session.refresh(data)
            result = self.select(
                session=session,
                query=LikeQuery(id=data.id),
                limit=1,
                offset=0,
            )
            return result[0]
        return None