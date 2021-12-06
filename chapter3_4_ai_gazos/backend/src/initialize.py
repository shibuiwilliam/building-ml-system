import json
from datetime import datetime
from logging import getLogger

from sqlalchemy import Column, Index
from sqlalchemy.engine import Engine
from src.configurations import Configurations
from src.entities.animal import AnimalCreate, AnimalQuery
from src.entities.user import UserCreate, UserQuery
from src.registry.container import container
from src.schema.base import Base
from src.schema.content import Content
from src.schema.like import Like
from src.schema.user import User

logger = getLogger(__name__)


def create_tables(checkfirst: bool = True):
    logger.info("create tables")
    engine = container.database.engine
    Base.metadata.create_all(
        engine,
        checkfirst=checkfirst,
        tables=[
            AnimalCategory.__table__,
            AnimalSubcategory.__table__,
            User.__table__,
            Animal.__table__,
            Like.__table__,
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


def create_indices(checkfirst: bool = True):
    logger.info("create indices")
    engine = container.database.engine
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
    create_index(
        table=Like,
        column=Like.animal_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=Like,
        column=Like.user_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    logger.info("done create indices")


def initialize_user():
    logger.info(f"initialize user: {Configurations.user_file}")
    with open(Configurations.user_file, "r") as f:
        data = json.load(f)
    session = container.database.get_session().__next__()
    for k, v in data.items():
        query = UserQuery(id=k)
        exist = container.user_repository.select(
            session=session,
            query=query,
            limit=1,
            offset=0,
        )
        if len(exist) > 0:
            continue
        record = UserCreate(
            id=k,
            handle_name=v["handle_name"],
            email_address=v["email_address"],
            age=v["age"],
            gender=v["gender"],
            created_at=datetime.strptime(v["created_at"], "%Y-%m-%dT%H:%M:%S.%f"),
        )
        container.user_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
    logger.info("done initialize user")


def initialize_animal():
    logger.info(f"initialize animal: {Configurations.animal_file}")
    with open(Configurations.animal_file, "r") as f:
        data = json.load(f)
    session = container.database.get_session().__next__()
    for k, v in data.items():
        query = AnimalQuery(id=k)
        exist = container.animal_reposigory.select(
            session=session,
            query=query,
            limit=1,
            offset=0,
        )
        if len(exist) > 0:
            continue
        record = AnimalCreate(
            id=k,
            animal_category_id=v["category"],
            animal_subcategory_id=v["subcategory"],
            user_id=v["user_id"],
            photo_url=v["photo_url"],
            name=v["filename"],
            description="",
            created_at=datetime.strptime(v["created_at"], "%Y-%m-%dT%H:%M:%S.%f"),
        )
        container.animal_reposigory.insert(
            session=session,
            record=record,
            commit=True,
        )
    logger.info("done initialize user")


def initialize_data():
    initialize_category()
    initialize_subcategory()
    initialize_user()
    initialize_animal()
