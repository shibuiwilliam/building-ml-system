import json
from datetime import datetime
from typing import List

from sqlalchemy.engine import Engine
from src.configurations import Configurations
from src.job.abstract_job import AbstractJob
from src.middleware.logger import configure_logger
from src.request_object.animal import AnimalCreateRequest
from src.request_object.animal_category import AnimalCategoryCreateRequest
from src.request_object.animal_subcategory import AnimalSubcategoryCreateRequest
from src.request_object.user import UserCreateRequest
from src.schema.animal import Animal
from src.schema.animal_category import AnimalCategory
from src.schema.animal_subcategory import AnimalSubcategory
from src.schema.base import Base
from src.schema.like import Like
from src.schema.user import User
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase
from src.usecase.animal_subcategory_usecase import AbstractAnimalSubcategoryUsecase
from src.usecase.animal_usecase import AbstractAnimalUsecase
from src.usecase.table_usecase import AbstractTableUsecase
from src.usecase.user_usecase import AbstractUserUsecase

logger = configure_logger(__name__)


class InitializationJob(AbstractJob):
    def __init__(
        self,
        table_usecase: AbstractTableUsecase,
        animal_category_usecase: AbstractAnimalCategoryUsecase,
        animal_subcategory_usecase: AbstractAnimalSubcategoryUsecase,
        user_usecase: AbstractUserUsecase,
        animal_usecase: AbstractAnimalUsecase,
        engine: Engine,
    ):
        super().__init__()
        self.table_usecase = table_usecase
        self.animal_category_usecase = animal_category_usecase
        self.animal_subcategory_usecase = animal_subcategory_usecase
        self.user_usecase = user_usecase
        self.animal_usecase = animal_usecase
        self.engine = engine

    def __create_table(self):
        tables: List[Base] = [AnimalCategory, AnimalSubcategory, User, Animal, Like]
        for table in tables:
            logger.info(f"create table: {table.__table__}")
            self.table_usecase.create_table(
                engine=self.engine,
                table=table,
                checkfirst=True,
            )
            logger.info(f"done create table: {table.__table__}")

    def __create_index(self):
        animal_category_indices = [
            {"column": AnimalCategory.name_en, "unique": True},
            {"column": AnimalCategory.name_ja, "unique": True},
            {"column": AnimalCategory.is_deleted, "unique": False},
        ]
        animal_subcategory_indices = [
            {"column": AnimalSubcategory.name_en, "unique": True},
            {"column": AnimalSubcategory.name_ja, "unique": True},
            {"column": AnimalSubcategory.animal_category_id, "unique": False},
            {"column": AnimalSubcategory.is_deleted, "unique": False},
        ]
        user_indices = [
            {"column": User.handle_name, "unique": False},
            {"column": User.email_address, "unique": True},
            {"column": User.deactivated, "unique": False},
        ]
        animal_indices = [
            {"column": Animal.name, "unique": False},
            {"column": Animal.user_id, "unique": False},
            {"column": Animal.animal_category_id, "unique": False},
            {"column": Animal.animal_subcategory_id, "unique": False},
        ]
        like_indices = [
            {"column": Like.user_id, "unique": False},
            {"column": Like.animal_id, "unique": False},
        ]

        for index in animal_category_indices:
            logger.info(f"create index: {index}")
            self.table_usecase.create_index(
                engine=self.engine,
                table=AnimalCategory,
                column=index["column"],
                checkfirst=True,
                unique=index["unique"],
            )
            logger.info(f"done create index: {index}")
        for index in animal_subcategory_indices:
            logger.info(f"create index: {index}")
            self.table_usecase.create_index(
                engine=self.engine,
                table=AnimalSubcategory,
                column=index["column"],
                checkfirst=True,
                unique=index["unique"],
            )
            logger.info(f"done create index: {index}")
        for index in user_indices:
            logger.info(f"create index: {index}")
            self.table_usecase.create_index(
                engine=self.engine,
                table=User,
                column=index["column"],
                checkfirst=True,
                unique=index["unique"],
            )
            logger.info(f"done create index: {index}")
        for index in animal_indices:
            logger.info(f"create index: {index}")
            self.table_usecase.create_index(
                engine=self.engine,
                table=Animal,
                column=index["column"],
                checkfirst=True,
                unique=index["unique"],
            )
            logger.info(f"done create index: {index}")
        for index in like_indices:
            logger.info(f"create index: {index}")
            self.table_usecase.create_index(
                engine=self.engine,
                table=Like,
                column=index["column"],
                checkfirst=True,
                unique=index["unique"],
            )
            logger.info(f"done create index: {index}")

    def __register_animal_category(
        self,
        file_path: str,
    ):
        logger.info(f"register animal category: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
        for k, v in data.items():
            logger.info(f"animal category {k} {v}")
            request = AnimalCategoryCreateRequest(
                id=v["category"],
                name_en=v["name_en"],
                name_ja=v["name_ja"],
            )
            self.animal_category_usecase.register(request=request)
        logger.info(f"done register animal category: {file_path}")

    def __register_animal_subcategory(
        self,
        file_path: str,
    ):
        logger.info(f"register animal subcategory: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
        for k, v in data.items():
            logger.info(f"animal subcategory {k} {v}")
            request = AnimalSubcategoryCreateRequest(
                id=v["subcategory"],
                animal_category_id=v["category"],
                name_en=v["name_en"],
                name_ja=v["name_ja"],
            )
            self.animal_subcategory_usecase.register(request=request)
        logger.info(f"done register animal subcategory: {file_path}")

    def __register_user(
        self,
        file_path: str,
    ):
        logger.info(f"register user: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
        for k, v in data.items():
            request = UserCreateRequest(
                id=k,
                handle_name=v["handle_name"],
                email_address=v["email_address"],
                password=v["password"],
                age=v["age"],
                gender=v["gender"],
                created_at=datetime.strptime(v["created_at"], "%Y-%m-%dT%H:%M:%S.%f"),
            )
            self.user_usecase.register(request=request)
        logger.info(f"done register user: {file_path}")

    def __register_animal(
        self,
        file_path: str,
    ):
        logger.info(f"register animal: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
        for k, v in data.items():
            request = AnimalCreateRequest(
                id=k,
                animal_category_id=v["category"],
                animal_subcategory_id=v["subcategory"],
                user_id=v["user_id"],
                name=v["filename"],
                description=v["description"],
                photo_url=v["photo_url"],
                created_at=datetime.strptime(v["created_at"], "%Y-%m-%dT%H:%M:%S.%f"),
            )
            self.animal_usecase.register(request=request)
        logger.info(f"done register animal: {file_path}")

    def run(self):
        logger.info("run initialize database")
        self.__create_table()
        self.__create_index()
        self.__register_animal_category(file_path=Configurations.animal_category_file)
        self.__register_animal_subcategory(file_path=Configurations.animal_subcategory_file)
        self.__register_user(file_path=Configurations.user_file)
        self.__register_animal(file_path=Configurations.animal_file)
