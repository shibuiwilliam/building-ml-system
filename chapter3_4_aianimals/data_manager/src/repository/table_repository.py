from abc import ABC, abstractmethod
from logging import getLogger

from sqlalchemy import Column, Index
from sqlalchemy.engine import Engine
from src.schema.base import Base

logger = getLogger(__name__)


class AbstractTableRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_table(
        self,
        engine: Engine,
        table: Base,
        checkfirst: bool = True,
    ):
        raise NotImplementedError

    @abstractmethod
    def create_index(
        table: Base,
        engine: Engine,
        column: Column,
        checkfirst: bool = True,
        unique: bool = False,
    ) -> Index:
        raise NotImplementedError
