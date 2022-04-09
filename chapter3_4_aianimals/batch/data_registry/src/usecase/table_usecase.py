import logging
from abc import ABC, abstractmethod

from sqlalchemy import Column, Index
from sqlalchemy.engine import Engine
from src.repository.table_repository import AbstractTableRepository
from src.schema.base import Base


class AbstractTableUsecase(ABC):
    def __init__(
        self,
        table_repository: AbstractTableRepository,
    ):
        self.logger = logging.getLogger(__name__)
        self.table_repository = table_repository

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
        self,
        engine: Engine,
        table: Base,
        column: Column,
        checkfirst: bool = True,
        unique: bool = False,
    ) -> Index:
        raise NotImplementedError


class TableUsecase(AbstractTableUsecase):
    def __init__(
        self,
        table_repository: AbstractTableRepository,
    ):
        super().__init__(table_repository=table_repository)

    def create_table(
        self,
        engine: Engine,
        table: Base,
        checkfirst: bool = True,
    ):
        self.table_repository.create_table(
            engine=engine,
            table=table,
            checkfirst=checkfirst,
        )

    def create_index(
        self,
        engine: Engine,
        table: Base,
        column: Column,
        checkfirst: bool = True,
        unique: bool = False,
    ) -> Index:
        return self.table_repository.create_index(
            engine=engine,
            table=table,
            column=column,
            checkfirst=checkfirst,
            unique=unique,
        )
