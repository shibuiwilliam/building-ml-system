import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extras import DictCursor
from src.dataset.schema import TABLES, Animal
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractDBClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_connection(self):
        raise NotImplementedError


class DBClient(AbstractDBClient):
    def __init__(self):
        self.__postgresql_user = os.environ["POSTGRESQL_USER"]
        self.__postgresql_password = os.environ["POSTGRESQL_PASSWORD"]
        self.__postgresql_port = int(os.getenv("POSTGRESQL_PORT", 5432))
        self.__postgresql_dbname = os.environ["POSTGRESQL_DBNAME"]
        self.__postgresql_host = os.environ["POSTGRESQL_HOST"]
        self.__connection_string = f"host={self.__postgresql_host} port={self.__postgresql_port} dbname={self.__postgresql_dbname} user={self.__postgresql_user} password={self.__postgresql_password}"

    def get_connection(self):
        return psycopg2.connect(self.__connection_string)


class BaseRepository(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client

    def execute_select_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> List[Dict[str, Any]]:
        logger.info(f"select query: {query}, parameters: {parameters}")
        with self.db_client.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, parameters)
                rows = cursor.fetchall()
        return rows


class AnimalRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.animal_table = TABLES.ANIMAL.value

    def select(
        self,
        limit: int = 1000,
        offset: int = 0,
    ) -> List[Animal]:
        query = f"""
SELECT
    {self.animal_table}.id AS id,
    {self.animal_table}.photo_url AS photo_url,
    {self.animal_table}.deactivated AS deactivated
FROM 
    {self.animal_table}
WHERE
    {self.animal_table}.deactivated = FALSE
LIMIT
    {limit}
OFFSET
    {offset}
;
        """

        records = self.execute_select_query(query=query)
        data = [Animal(**r) for r in records]
        return data

    def select_all(
        self,
    ) -> List[Animal]:
        limit = 1000
        offset = 0
        records = []
        while True:
            r = self.select(
                limit=limit,
                offset=offset,
            )
            if len(r) > 0:
                records.extend(r)
            else:
                break
            offset += limit
        return records
