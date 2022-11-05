from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from src.entities.common import Count
from src.entities.like import LikeCreate, LikeDelete, LikeModel, LikeQuery
from src.schema.like import Like
from src.schema.table import TABLES

logger = getLogger(__name__)


class AbstractLikeRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[LikeQuery] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[LikeModel]:
        raise NotImplementedError

    @abstractmethod
    def count(
        self,
        session: Session,
        animal_ids: List[str],
    ) -> Dict[str, Count]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: LikeCreate,
        commit: bool = True,
    ) -> Optional[LikeModel]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        session: Session,
        record: LikeDelete,
        commit: bool = True,
    ):
        raise NotImplementedError


class LikeRepository(AbstractLikeRepository):
    def __init__(self):
        super().__init__()
        self.table_name = TABLES.LIKE.value

    def select(
        self,
        session: Session,
        query: Optional[LikeQuery] = None,
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
        data = {animal_id: Count(count=0) for animal_id in animal_ids}
        for r in results:
            data[r["animal_id"]] = Count(count=r["count"])
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
