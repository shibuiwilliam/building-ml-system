from logging import getLogger

from sqlalchemy import Column, Index
from sqlalchemy.engine import Engine
from src.repository.table_repository import AbstractTableRepository
from src.schema.base import Base

logger = getLogger(__name__)


class TableRepository(AbstractTableRepository):
    def __init__(self):
        pass

    def create_table(
        self,
        engine: Engine,
        table: Base,
        checkfirst: bool = True,
    ):
        logger.info(f"create table: {table.__table__}")
        Base.metadata.create_all(
            engine,
            checkfirst=checkfirst,
            tables=[table.__table__],
        )
        logger.info(f"done create table: {table.__table__}")

    def create_index(
        table: Base,
        engine: Engine,
        column: Column,
        checkfirst: bool = True,
        unique: bool = False,
    ) -> Index:
        index_name = f"{table.__tablename__}_{column.name}_index"
        logger.info(f"create index: {index_name}")
        index = Index(
            index_name,
            column,
            unique=unique,
        )
        index.create(
            bind=engine,
            checkfirst=checkfirst,
        )
        logger.info(f"done create index: {index_name}")
        return index
