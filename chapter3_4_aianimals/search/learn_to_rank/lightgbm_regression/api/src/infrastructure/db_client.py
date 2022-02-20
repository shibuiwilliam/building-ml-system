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
        self.__postgresql_user = os.environ["POSTGRESQL_USER"]
        self.__postgresql_password = os.environ["POSTGRESQL_PASSWORD"]
        self.__postgresql_port = int(os.getenv("POSTGRESQL_PORT", 5432))
        self.__postgresql_dbname = os.environ["POSTGRESQL_DBNAME"]
        self.__postgresql_host = os.environ["POSTGRESQL_HOST"]
        self.__connection_string = f"host={self.__postgresql_host} port={self.__postgresql_port} dbname={self.__postgresql_dbname} user={self.__postgresql_user} password={self.__postgresql_password}"

    def get_connection(self):
        return psycopg2.connect(self.__connection_string)
