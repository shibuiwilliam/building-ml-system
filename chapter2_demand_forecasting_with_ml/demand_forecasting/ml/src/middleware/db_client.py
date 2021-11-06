from abc import ABC, abstractmethod

import psycopg2
from configurations import DatabaseConfigurations
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
        self.__connection_string = DatabaseConfigurations.connection_string

    def get_connection(self):
        return psycopg2.connect(self.__connection_string)
