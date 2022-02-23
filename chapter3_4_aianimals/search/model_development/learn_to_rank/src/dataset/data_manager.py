import os
from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extras import DictCursor
from src.dataset.schema import TABLES, AccessLog
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
        self.__postgresql_user = os.environ["POSTGRES_USER"]
        self.__postgresql_password = os.environ["POSTGRES_PASSWORD"]
        self.__postgresql_port = int(os.getenv("POSTGRES_PORT", 5432))
        self.__postgresql_dbname = os.environ["POSTGRES_DBNAME"]
        self.__postgresql_host = os.environ["POSTGRES_HOST"]
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


class AccessLogRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.access_log_table = TABLES.ACCESS_LOG.value
        self.animal_table = TABLES.ANIMAL.value

    def select(
        self,
        date_from: Optional[date] = None,
        limit: int = 1000,
        offset: int = 0,
    ) -> List[AccessLog]:
        parameters = []
        query = f"""
SELECT
    {self.access_log_table}.id AS id,
    {self.access_log_table}.phrases AS query_phrases,
    {self.access_log_table}.animal_category_id AS query_animal_category_id,
    {self.access_log_table}.animal_subcategory_id AS query_animal_subcategory_id,
    {self.access_log_table}.user_id AS user_id,
    {self.access_log_table}.likes AS likes,
    {self.access_log_table}.action AS action,
    {self.access_log_table}.animal_id AS animal_id,
    {self.animal_table}.animal_category_id AS animal_category_id,
    {self.animal_table}.animal_subcategory_id AS animal_subcategory_id,
    {self.animal_table}.name AS name,
    {self.animal_table}.description AS description
FROM 
    {self.access_log_table}
LEFT JOIN
    {self.animal_table}
ON
    {self.access_log_table}.animal_id = {self.animal_table}.id
        """

        if date_from is not None:
            query += f"""
WHERE
    {self.access_log_table}.created_at >= %s
            """
            parameters.append(date_from)

        query += f"""
ORDER BY
    {self.access_log_table}.created_at
LIMIT
    {limit}
OFFSET
    {offset}
;
"""

        records = self.execute_select_query(
            query=query,
            parameters=parameters,
        )
        data = [AccessLog(**r) for r in records]
        return data

    def select_all(
        self,
        date_from: Optional[date] = None,
    ) -> List[AccessLog]:
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
