import os
from abc import ABC, abstractmethod
from logging import getLogger

import psycopg2

logger = getLogger(__name__)


class AbstractDBClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_connection(self):
        raise NotImplementedError


class DBClient(AbstractDBClient):
    def __init__(self):
        self.__postgres_user = os.environ["POSTGRES_USER"]
        self.__postgres_password = os.environ["POSTGRES_PASSWORD"]
        self.__postgres_port = int(os.getenv("POSTGRES_PORT", 5432))
        self.__postgres_db = os.environ["POSTGRES_DB"]
        self.__postgres_host = os.environ["POSTGRES_HOST"]
        self.__connection_string = f"host={self.__postgres_host} port={self.__postgres_port} dbname={self.__postgres_db} user={self.__postgres_user} password={self.__postgres_password}"

    def get_connection(self):
        return psycopg2.connect(self.__connection_string)
