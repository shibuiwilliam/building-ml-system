from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from psycopg2 import extras
from psycopg2.extras import DictCursor
from pydantic import BaseModel
from src.exceptions.exceptions import DatabaseException
from src.infrastructure.database import AbstractDBClient
from src.middleware.logger import configure_logger
from src.model.abstract_model import AbstractModel

logger = configure_logger(__name__)


class AbstractQuery(BaseModel):
    pass


class AbstractRepository(ABC):
    def __init__(self):
        self.table_name: str = ""
        self.columns: List[str] = []

    @abstractmethod
    def insert(
        self,
        record: AbstractModel,
    ):
        raise NotImplementedError

    @abstractmethod
    def select(
        self,
        condition: Optional[AbstractQuery] = None,
    ) -> List[AbstractModel]:
        raise NotImplementedError


class BaseRepository(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client

    def execute_create_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ):
        logger.debug(f"create query: {query}, parameters: {parameters}")
        with self.db_client.get_connection() as conn:
            try:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query, parameters)
                conn.commit()
            except psycopg2.Error as e:
                conn.rollback()
                raise DatabaseException(
                    message=f"failed to insert or update query: {e}",
                    detail=f"{query} {parameters}: {e}",
                )

    def execute_insert_or_update_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ):
        logger.debug(f"insert or update query: {query}, parameters: {parameters}")
        with self.db_client.get_connection() as conn:
            try:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query, parameters)
                conn.commit()
            except psycopg2.Error as e:
                conn.rollback()
                raise DatabaseException(
                    message=f"failed to insert or update query: {e}",
                    detail=f"{query} {parameters}: {e}",
                )

    def execute_bulk_insert_or_update_query(
        self,
        query: str,
        parameters: Optional[List[Tuple]] = None,
    ) -> bool:
        logger.debug(f"bulk insert or update query: {query}, parameters: {parameters}")
        with self.db_client.get_connection() as conn:
            try:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    extras.execute_values(cursor, query, parameters)
                conn.commit()
                return True
            except psycopg2.Error as e:
                conn.rollback()
                raise DatabaseException(
                    message=f"failed to bulk insert or update query: {e}",
                    detail=f"{query} {parameters}: {e}",
                )

    def execute_delete_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ):
        logger.info(f"delete query: {query} parameters: {parameters}")
        with self.db_client.get_connection() as conn:
            try:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query, parameters)
                conn.commit()
            except psycopg2.Error as e:
                conn.rollback()
                raise DatabaseException(
                    message=f"failed to delete query: {e}",
                    detail=f"{query} {parameters}: {e}",
                )

    def execute_select_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> List[Dict[str, Any]]:
        logger.debug(f"select query: {query}, parameters: {parameters}")
        with self.db_client.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, parameters)
                rows = cursor.fetchall()
        return rows
