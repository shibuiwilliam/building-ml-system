import json
from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy import and_
from src.entities.animal_feature import AnimalFeatureCreate, AnimalFeatureModel, AnimalFeatureQuery, AnimalFeatureUpdate
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger
from src.schema.animal_feature import AnimalFeature
from src.schema.table import TABLES

logger = configure_logger(__name__)


class AbstractAnimalFeatureRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.database = database

    @abstractmethod
    def select(
        self,
        query: Optional[AnimalFeatureQuery],
        limit: int = 100,
        offset: int = 0,
    ) -> List[AnimalFeatureModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        record: AnimalFeatureCreate,
        commit: bool = True,
    ):
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        record: AnimalFeatureUpdate,
    ):
        raise NotImplementedError

    @abstractmethod
    def bulk_insert(
        self,
        records: List[AnimalFeatureCreate],
        commit: bool = True,
    ):
        raise NotImplementedError


class AnimalFeatureRepository(AbstractAnimalFeatureRepository):
    def __init__(
        self,
        database: AbstractDatabase,
    ) -> None:
        super().__init__(database=database)
        self.table_name = TABLES.ANIMAL_FEATURE.value

    def select(
        self,
        query: Optional[AnimalFeatureQuery],
        limit: int = 100,
        offset: int = 0,
    ) -> List[AnimalFeatureModel]:
        session = self.database.get_session().__next__()
        try:
            filters = []
            if query is not None and len(query.ids) > 0:
                filters.append(AnimalFeature.id.in_(query.ids))
            results = (
                session.query(AnimalFeature)
                .filter(and_(*filters))
                .order_by(AnimalFeature.id)
                .limit(limit)
                .offset(offset)
            )
            data = [
                AnimalFeatureModel(
                    id=d.id,
                    name_words=d.name_words,
                    name_vector=d.name_vector,
                    description_words=d.description_words,
                    description_vector=d.description_vector,
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

    def insert(
        self,
        record: AnimalFeatureCreate,
        commit: bool = True,
    ):
        session = self.database.get_session().__next__()
        try:
            data = record.dict()
            data["name_words"] = data["name_words"]
            data["name_vector"] = data["name_vector"]
            data["description_words"] = data["description_words"]
            data["description_vector"] = data["description_vector"]
            data = AnimalFeature(**data)
            session.add(data)
            if commit:
                session.commit()
        except Exception as e:
            raise e
        finally:
            session.close()

    def update(
        self,
        record: AnimalFeatureUpdate,
    ):
        session = self.database.get_session().__next__()
        try:
            updates = {}
            if record.name_words is not None:
                updates["name_words"] = record.name_words
            if record.name_vector is not None:
                updates["name_vector"] = record.name_vector
            if record.description_words is not None:
                updates["description_words"] = record.description_words
            if record.description_vector is not None:
                updates["description_vector"] = record.description_vector
            session.query(AnimalFeature).filter(AnimalFeature.id == record.id).update(updates)
            session.commit()
        except Exception as e:
            raise e
        finally:
            session.close()

    def bulk_insert(
        self,
        records: List[AnimalFeatureCreate],
        commit: bool = True,
    ):
        session = self.database.get_session().__next__()
        try:
            data = [d.dict() for d in records]
            session.execute(AnimalFeature.__table__.insert(), data)
            if commit:
                session.commit()
        except Exception as e:
            raise e
        finally:
            session.close()
