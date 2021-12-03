from logging import getLogger
from typing import Dict, List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from src.entities.common import Count
from src.entities.like import LikeCreate, LikeDelete, LikeModel, LikeQuery
from src.repository.like_repository import AbstractLikeRepository
from src.schema.like import Like
from src.schema.table import TABLES

logger = getLogger(__name__)


class LikeRepository(AbstractLikeRepository):
    def __init__(self) -> None:
        super().__init__()
        self.table_name = TABLES.LIKE.value

    def select(
        self,
        session: Session,
        query: Optional[LikeQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[LikeModel]:
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(Like.id == query.id)
            if query.animal_id is not None:
                filters.append(Like.animal_id == query.animal_id)
            if query.user_id is not None:
                filters.append(Like.id == query.user_id)
        results = session.query(Like).filter(and_(*filters)).order_by(Like.id).limit(limit).offset(offset)
        data = [
            LikeModel(
                id=d[0],
                animal_id=d[1],
                user_id=d[2],
                created_at=d[3],
                updated_at=d[4],
            )
            for d in results
        ]
        return data

    def count(
        self,
        session: Session,
        animal_ids: List[str],
    ) -> Dict[str, Count]:
        results = (
            session.query(
                func.count(Like.id).label("count"),
                Like.animal_id.label("animal_id"),
            )
            .filter(Like.animal_id.in_(animal_ids))
            .group_by(Like.animal_id)
            .order_by(Like.animal_id)
            .all()
        )
        data = {r["animal_id"]: Count(count=r["count"]) for r in results}
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

    def delete(
        self,
        session: Session,
        record: LikeDelete,
        commit: bool = True,
    ):
        results = session.query(Like).filter(Like.id == record.id).all()
        for r in results:
            session.delete(r)
            if commit:
                session.commit()
