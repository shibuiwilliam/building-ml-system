from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extras import DictCursor
from src.configurations import Configurations
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
        self.__connection_string = Configurations.connection_string

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
        limit: int = 200,
        offset: int = 0,
    ) -> List[AccessLog]:
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
LIMIT
    {limit}
OFFSET
    {offset}
;
        """

        records = self.execute_select_query(query=query)
        data = [AccessLog(**r) for r in records]
        return data

    def select_all(
        self,
    ) -> List[AccessLog]:
        limit = 200
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
