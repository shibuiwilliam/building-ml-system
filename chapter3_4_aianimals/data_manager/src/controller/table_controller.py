from abc import ABC, abstractmethod

from sqlalchemy.engine import Engine
from src.middleware.logger import configure_logger
from src.usecase.table_usecase import AbstractTableUsecase

logger = configure_logger(__name__)


class AbstractTableController(ABC):
    def __init__(
        self,
        table_usecase: AbstractTableUsecase,
        engine: Engine,
    ):
        self.table_usecase = table_usecase
        self.engine = engine

    @abstractmethod
    def create_table(self):
        raise NotImplementedError

    @abstractmethod
    def create_index(self):
        raise NotImplementedError
