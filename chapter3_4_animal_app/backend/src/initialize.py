from logging import getLogger

from sqlalchemy import Column, Index
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from src.middleware.database import Base
from src.repository.animal_category_repository import AnimalCategory
from src.repository.animal_repository import Animal
from src.repository.animal_subcategory_repository import AnimalSubcategory
from src.repository.user_repository import User

logger = getLogger(__name__)


def create_tables(
    engine: Engine,
    checkfirst: bool = True,
):
    logger.info("create tables")
    Base.metadata.create_all(
        engine,
        checkfirst=checkfirst,
        tables=[
            AnimalCategory.__table__,
            AnimalSubcategory.__table__,
            User.__table__,
            Animal.__table__,
        ],
    )
    logger.info("done create tables")


def create_index(
    table: Base,
    column: Column,
    engine: Engine,
    checkfirst: bool = True,
    unique: bool = False,
) -> Index:
    index_name = f"{table.__tablename__}_{column.name}_index"
    index = Index(
        index_name,
        column,
        unique=unique,
    )
    index.create(
        bind=engine,
        checkfirst=checkfirst,
    )
    logger.info(f"created index: {index_name}")
    return index


def create_indices(
    engine: Engine,
    checkfirst: bool = True,
):
    logger.info("create indices")
    create_index(
        table=AnimalCategory,
        column=AnimalCategory.name,
        engine=engine,
        checkfirst=checkfirst,
        unique=True,
    )
    create_index(
        table=AnimalCategory,
        column=AnimalCategory.is_deleted,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )

    create_index(
        table=AnimalSubcategory,
        column=AnimalSubcategory.animal_category_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=AnimalSubcategory,
        column=AnimalSubcategory.name,
        engine=engine,
        checkfirst=checkfirst,
        unique=True,
    )
    create_index(
        table=AnimalSubcategory,
        column=AnimalSubcategory.is_deleted,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )

    create_index(
        table=User,
        column=User.handle_name,
        engine=engine,
        checkfirst=checkfirst,
        unique=True,
    )
    create_index(
        table=User,
        column=User.deactivated,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )

    create_index(
        table=Animal,
        column=Animal.name,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=Animal,
        column=Animal.animal_category_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=Animal,
        column=Animal.animal_subcategory_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=Animal,
        column=Animal.user_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=Animal,
        column=Animal.deactivated,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    logger.info("done create indices")
