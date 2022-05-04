import logging
from abc import ABC, abstractmethod
from typing import List

from src.entities.access_log import AccessLog
from src.infrastructure.database import AbstractDBClient
from src.repository.base_repository import BaseRepository
from src.repository.table import TABLES


class AbstractAccessLogRepository(ABC):
    def __init__(self):
        self.table_name = TABLES.ACCESS_LOG.value

    @abstractmethod
    def select(
        self,
        limit: int = 200,
        offset: int = 0,
    ) -> List[AccessLog]:
        raise NotImplementedError


class AccessLogRepository(BaseRepository, AbstractAccessLogRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        BaseRepository.__init__(self, db_client=db_client)
        AbstractAccessLogRepository.__init__(self)

    def select(
        self,
        limit: int = 200,
        offset: int = 0,
    ) -> List[AccessLog]:
        query = f"""
        SELECT
            {self.table_name}.phrases
        FROM
            {self.table_name}
        LIMIT
            {limit}
        OFFSET
            {offset}
        ;
        """
        result = self.execute_select_query(
            query=query,
            parameters=None,
        )
        data = [AccessLog(**r) for r in result]
        return data
