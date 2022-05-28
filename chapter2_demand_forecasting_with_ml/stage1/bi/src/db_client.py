import os
from abc import ABC, abstractmethod

import psycopg2
from logger import configure_logger

logger = configure_logger(__name__)


class AbstractDBClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_connection(self):
        raise NotImplementedError


class PostgreSQLClient(AbstractDBClient):
    def __init__(self):
        self.__postgresql_user = os.getenv("POSTGRES_USER")
        self.__postgresql_password = os.getenv("POSTGRES_PASSWORD")
        self.__postgresql_port = int(os.getenv("POSTGRES_PORT", 5432))
        self.__postgresql_dbname = os.getenv("POSTGRES_DB")
        self.__postgresql_host = os.getenv("POSTGRES_HOST")
        self.__connection_string = f"host={self.__postgresql_host} port={self.__postgresql_port} dbname={self.__postgresql_dbname} user={self.__postgresql_user} password={self.__postgresql_password}"

    def get_connection(self):
        return psycopg2.connect(self.__connection_string)
