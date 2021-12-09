from sqlalchemy import Column, Index
from sqlalchemy.engine import Engine
from src.middleware.logger import configure_logger
from src.repository.table_repository import AbstractTableRepository
from src.schema.base import Base
from src.usecase.table_usecase import AbstractTableUsecase

logger = configure_logger(__name__)


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
