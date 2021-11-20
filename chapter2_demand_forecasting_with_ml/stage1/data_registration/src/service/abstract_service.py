from abc import ABC, abstractmethod

from src.middleware.database import AbstractDBClient


class AbstractService(ABC):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client
