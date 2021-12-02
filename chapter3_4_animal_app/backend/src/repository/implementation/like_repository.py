from logging import getLogger
from typing import Dict, List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, String, and_
from sqlalchemy.func import count
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
from src.middleware.database import Base
from src.repository.abstract_repository import AbstractRepository
from src.schema.like import LikeCreate, LikeModel, LikeQuery
from src.schema.schema import Count
from src.schema.table import TABLES

logger = getLogger(__name__)


class Like(Base):
    __tablename__ = TABLES.LIKE.value
    id = Column(
        String(32),
        primary_key=True,
    )
    animal_id = Column(
        String(32),
        ForeignKey(f"{TABLES.ANIMAL.value}.id"),
        nullable=False,
        unique=False,
    )
    user_id = Column(
        String(32),
        ForeignKey(f"{TABLES.USER.value}.id"),
        nullable=False,
        unique=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )


class LikeRepository(AbstractRepository):
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
        data = [LikeModel(**(self.model_to_dict(d))) for d in results]
        return data

    def count(
        self,
        session: Session,
        animal_ids: List[str],
    ) -> Dict[str, Count]:
        results = (
            session.query(
                count(Like.id).label("count"),
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
                query=LikeQuery(
                    id=data.id,
                    limit=1,
                    offset=0,
                ),
            )
            return result[0]
        return None
