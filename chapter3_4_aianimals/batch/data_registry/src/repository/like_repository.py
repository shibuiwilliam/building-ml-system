import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from sqlalchemy import and_, func
from src.entities.common import Count
from src.entities.like import LikeCreate, LikeModel, LikeQuery
from src.infrastructure.database import AbstractDatabase
from src.schema.like import Like
from src.schema.table import TABLES


class AbstractLikeRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.logger = logging.getLogger(__name__)
        self.database = database

    @abstractmethod
    def select(
        self,
        query: Optional[LikeQuery],
        limit: int = 100,
        offset: int = 0,
    ) -> List[LikeModel]:
        raise NotImplementedError

    @abstractmethod
    def count(
        self,
        animal_ids: List[str],
    ) -> Dict[str, Count]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        record: LikeCreate,
        commit: bool = True,
    ) -> Optional[LikeModel]:
        raise NotImplementedError

    @abstractmethod
    def bulk_insert(
        self,
        records: List[LikeCreate],
        commit: bool = True,
    ):
        raise NotImplementedError


class LikeRepository(AbstractLikeRepository):
    def __init__(
        self,
        database: AbstractDatabase,
    ) -> None:
        super().__init__(database=database)
        self.table_name = TABLES.LIKE.value

    def select(
        self,
        query: Optional[LikeQuery],
        limit: int = 100,
        offset: int = 0,
    ) -> List[LikeModel]:
        session = self.database.get_session().__next__()
        try:
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
        except Exception as e:
            raise e
        finally:
            session.close()

    def count(
        self,
        animal_ids: List[str],
    ) -> Dict[str, Count]:
        session = self.database.get_session().__next__()
        try:
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
        except Exception as e:
            raise e
        finally:
            session.close()

    def insert(
        self,
        record: LikeCreate,
        commit: bool = True,
    ) -> Optional[LikeModel]:
        session = self.database.get_session().__next__()
        try:
            data = Like(**record.dict())
            session.add(data)
            if commit:
                session.commit()
                session.refresh(data)
                result = self.select(
                    query=LikeQuery(id=data.id),
                    limit=1,
                    offset=0,
                )
                return result[0]
            return None
        except Exception as e:
            raise e
        finally:
            session.close()

    def bulk_insert(
        self,
        records: List[LikeCreate],
        commit: bool = True,
    ):
        session = self.database.get_session().__next__()
        try:
            data = [d.dict() for d in records]
            session.execute(Like.__table__.insert(), data)
            if commit:
                session.commit()
        except Exception as e:
            raise e
        finally:
            session.close()
