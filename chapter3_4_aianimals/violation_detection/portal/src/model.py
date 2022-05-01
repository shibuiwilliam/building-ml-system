import logging
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

import psycopg2
from database import AbstractDBClient
from psycopg2.extras import DictCursor
from pydantic import BaseModel, Extra


class TABLES(Enum):
    ANIMAL = "animals"
    VIOLATION_TYPE = "violation_types"
    VIOLATION = "violations"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in TABLES.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in TABLES.__members__.values()]


class AnimalQuery(BaseModel):
    ids: Optional[List[str]] = None

    class Config:
        extra = Extra.forbid


class Animal(BaseModel):
    id: str
    name: str
    animal_category_id: int
    animal_subcategory_id: int
    description: str
    photo_url: str
    deactivated: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class ViolationType(BaseModel):
    id: str
    name: str

    class Config:
        extra = Extra.forbid


class ViolationQuery(BaseModel):
    ids: Optional[List[str]] = None
    animal_id: Optional[str] = None
    violation_type_id: Optional[str] = None
    judge: Optional[str] = None
    is_effective: Optional[bool] = None
    animal_days_from: Optional[int] = None
    days_from: Optional[int] = None

    class Config:
        extra = Extra.forbid


class Violation(BaseModel):
    id: str
    animal_id: str
    animal_name: str
    violation_type_name: str
    judge: str
    probability: float
    is_effective: bool
    animal_created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class VIOLATION_SORT_BY(Enum):
    UPDATED_AT = "updated_at"
    ANIMAL_CREATED_AT = "animal_created_at"
    ID = "id"
    ANIMAL_ID = "animal_id"
    VIOLATION_TYPE_NAME = "violation_type_name"
    JUDGE = "judge"
    PROBABILITY = "probability"
    IS_EFFECTIVE = "is_effective"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in VIOLATION_SORT_BY.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in VIOLATION_SORT_BY.__members__.values()]


class BaseRepository(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client
        self.logger = logging.getLogger(__name__)

    def execute_select_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> List[Dict[str, Any]]:
        self.logger.info(f"select query: {query}, parameters: {parameters}")
        with self.db_client.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, parameters)
                rows = cursor.fetchall()
        return rows

    def execute_insert_or_update_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> bool:
        self.logger.debug(f"insert or update query: {query}, parameters: {parameters}")
        with self.db_client.get_connection() as conn:
            try:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query, parameters)
                conn.commit()
                return True
            except psycopg2.Error as e:
                conn.rollback()
                raise e


class AbstractAnimalRepository(ABC):
    def __init__(self):
        self.animal_table = TABLES.ANIMAL.value

    @abstractmethod
    def select(
        self,
        animal_query: AnimalQuery,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Animal]:
        raise NotImplementedError


class AnimalRepository(BaseRepository, AbstractAnimalRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        BaseRepository.__init__(self, db_client=db_client)
        AbstractAnimalRepository.__init__(self)

    def select(
        self,
        animal_query: AnimalQuery,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Animal]:
        parameters = []

        query = f"""
            SELECT
                {self.animal_table}.id,
                {self.animal_table}.name,
                {self.animal_table}.animal_category_id,
                {self.animal_table}.animal_subcategory_id,
                {self.animal_table}.description,
                {self.animal_table}.photo_url,
                {self.animal_table}.deactivated,
                {self.animal_table}.created_at,
                {self.animal_table}.updated_at
            FROM 
                {self.animal_table}
        """

        if animal_query is not None:
            if animal_query.ids is not None and len(animal_query.ids) > 0:
                parameters.extend(animal_query.ids)
                ids = ",".join(["%s" for _ in animal_query.ids])
                query += f"""
                WHERE
                    {self.animal_table}.id IN ({ids})
                """

        query += f"""
            LIMIT
                {limit}
            OFFSET
                {offset}
            ;
        """

        records = self.execute_select_query(
            query=query,
            parameters=tuple(parameters),
        )
        data = [Animal(**r) for r in records]
        return data


class AbstractViolationTypeRepository(ABC):
    def __init__(self):
        self.violation_type_table = TABLES.VIOLATION_TYPE.value

    @abstractmethod
    def select(
        self,
        limit: int = 200,
        offset: int = 0,
    ) -> List[ViolationType]:
        raise NotImplementedError


class ViolationTypeRepository(BaseRepository, AbstractViolationTypeRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        BaseRepository.__init__(self, db_client=db_client)
        AbstractViolationTypeRepository.__init__(self)

    def select(
        self,
        limit: int = 200,
        offset: int = 0,
    ) -> List[ViolationType]:
        query = f"""
            SELECT
                {self.violation_type_table}.id,
                {self.violation_type_table}.name
            FROM 
                {self.violation_type_table}
            LIMIT
                {limit}
            OFFSET
                {offset}
            ;
        """

        records = self.execute_select_query(
            query=query,
            parameters=None,
        )
        data = [ViolationType(**r) for r in records]
        return data


class AbstractViolationRepository(ABC):
    def __init__(self):
        self.violation_table = TABLES.VIOLATION.value
        self.violation_type_table = TABLES.VIOLATION_TYPE.value
        self.animal_table = TABLES.ANIMAL.value

    @abstractmethod
    def select(
        self,
        violation_query: Optional[ViolationQuery] = None,
        sort_by: str = VIOLATION_SORT_BY.ID.value,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Violation]:
        raise NotImplementedError


class ViolationRepository(BaseRepository, AbstractViolationRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        BaseRepository.__init__(self, db_client=db_client)
        AbstractViolationRepository.__init__(self)

    def select(
        self,
        violation_query: Optional[ViolationQuery] = None,
        sort_by: str = VIOLATION_SORT_BY.ID.value,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Violation]:
        parameters: List[Union[str, int, bool, float]] = []
        query = f"""
            SELECT
                {self.violation_table}.id AS id,
                {self.animal_table}.id AS animal_id,
                {self.animal_table}.name AS animal_name,
                {self.violation_type_table}.name AS violation_type_name,
                {self.violation_table}.judge AS judge,
                {self.violation_table}.probability AS probability,
                {self.violation_table}.is_effective AS is_effective,
                {self.animal_table}.created_at AS animal_created_at,
                {self.violation_table}.updated_at AS updated_at
            FROM 
                {self.violation_table}
            LEFT JOIN
                {self.animal_table}
            ON
                {self.violation_table}.animal_id = {self.animal_table}.id
            LEFT JOIN
                {self.violation_type_table}
            ON
                {self.violation_table}.violation_type_id = {self.violation_type_table}.id
        """

        if violation_query is not None:
            where = "WHERE"
            if violation_query.ids is not None and len(violation_query.ids) > 0:
                p = ",".join("%s" for _ in violation_query.ids)
                parameters.extend(violation_query.ids)
                query += f"""
                {where} {self.violation_table}.id IN ({p})
                """
                where = "AND"
            if violation_query.animal_id is not None:
                parameters.append(violation_query.animal_id)
                query += f"""
                {where} {self.animal_table}.id = %s 
                """
                where = "AND"
            if violation_query.violation_type_id is not None:
                parameters.append(violation_query.violation_type_id)
                query += f"""
                {where} {self.violation_type_table}.id = %s
                """
                where = "AND"
            if violation_query.judge is not None:
                parameters.append(violation_query.judge)
                query += f"""
                {where} {self.violation_table}.judge = %s
                """
                where = "AND"
            if violation_query.is_effective is not None:
                parameters.append(violation_query.is_effective)
                query += f"""
                {where} {self.violation_table}.is_effective = %s
                """
                where = "AND"
            if violation_query.animal_days_from is not None:
                parameters.append(violation_query.animal_days_from)
                query += f"""
                {where} {self.animal_table}.created_at > NOW() - interval `%s DAY'
                """
                where = "AND"
            if violation_query.days_from is not None:
                parameters.append(violation_query.days_from)
                query += f"""
                {where} {self.violation_table}.updated_at > NOW() - interval '%s DAY'
                """

        query += f"""
            ORDER BY
                {sort_by}
            LIMIT
                {limit}
            OFFSET
                {offset}
            ;
        """

        records = self.execute_select_query(
            query=query,
            parameters=tuple(parameters),
        )
        data = [Violation(**r) for r in records]
        return data
