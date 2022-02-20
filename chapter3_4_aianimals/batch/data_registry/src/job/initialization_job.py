import json
from datetime import datetime
from re import I
from typing import Dict, List

from sqlalchemy.engine import Engine
from src.configurations import Configurations
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.job.abstract_job import AbstractJob
from src.middleware.logger import configure_logger
from src.request_object.access_log import AccessLogCreateRequest
from src.request_object.animal import AnimalCreateRequest
from src.request_object.animal_category import AnimalCategoryCreateRequest
from src.request_object.animal_subcategory import AnimalSubcategoryCreateRequest
from src.request_object.user import UserCreateRequest
from src.request_object.violation import ViolationCreateRequest
from src.request_object.violation_type import ViolationTypeCreateRequest
from src.schema.access_log import AccessLog
from src.schema.animal import Animal
from src.schema.animal_category import AnimalCategory
from src.schema.animal_subcategory import AnimalSubcategory
from src.schema.base import Base
from src.schema.like import Like
from src.schema.user import User
from src.schema.violation import Violation
from src.schema.violation_type import ViolationType
from src.usecase.access_log_usecase import AbstractAccessLogUsecase
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase
from src.usecase.animal_subcategory_usecase import AbstractAnimalSubcategoryUsecase
from src.usecase.animal_usecase import AbstractAnimalUsecase
from src.usecase.table_usecase import AbstractTableUsecase
from src.usecase.user_usecase import AbstractUserUsecase
from src.usecase.violation_type_usecase import AbstractViolationTypeUsecase
from src.usecase.violation_usecase import AbstractViolationUsecase

logger = configure_logger(__name__)


class InitializationJob(AbstractJob):
    def __init__(
        self,
        table_usecase: AbstractTableUsecase,
        animal_category_usecase: AbstractAnimalCategoryUsecase,
        animal_subcategory_usecase: AbstractAnimalSubcategoryUsecase,
        user_usecase: AbstractUserUsecase,
        animal_usecase: AbstractAnimalUsecase,
        violation_type_usecase: AbstractViolationTypeUsecase,
        violation_usecase: AbstractViolationUsecase,
        access_log_usecase: AbstractAccessLogUsecase,
        messaging: RabbitmqMessaging,
        engine: Engine,
    ):
        super().__init__()
        self.table_usecase = table_usecase
        self.animal_category_usecase = animal_category_usecase
        self.animal_subcategory_usecase = animal_subcategory_usecase
        self.user_usecase = user_usecase
        self.animal_usecase = animal_usecase
        self.violation_type_usecase = violation_type_usecase
        self.violation_usecase = violation_usecase
        self.access_log_usecase = access_log_usecase
        self.messaging = messaging
        self.engine = engine

    def __create_table(self):
        tables: List[Base] = [
            AnimalCategory,
            AnimalSubcategory,
            User,
            Animal,
            Like,
            ViolationType,
            Violation,
            AccessLog,
        ]
        for table in tables:
            logger.info(f"create table: {table.__table__}")
            self.table_usecase.create_table(
                engine=self.engine,
                table=table,
                checkfirst=True,
            )
            logger.info(f"done create table: {table.__table__}")

    def __create_index(
        self,
        indices: List[Dict],
        table: Base,
    ):
        for index in indices:
            logger.info(f"create index: {index}")
            self.table_usecase.create_index(
                engine=self.engine,
                table=table,
                column=index["column"],
                checkfirst=True,
                unique=index["unique"],
            )
            logger.info(f"done create index: {index}")

    def __create_indices(self):
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
        violation_type_indices = [
            {"column": ViolationType.name, "unique": True},
        ]
        violation_indices = [
            {"column": Violation.animal_id, "unique": False},
            {"column": Violation.violation_type_id, "unique": False},
            {"column": Violation.judge, "unique": False},
            {"column": Violation.probability, "unique": False},
            {"column": Violation.is_effective, "unique": False},
        ]

        self.__create_index(
            indices=animal_category_indices,
            table=AnimalCategory,
        )
        self.__create_index(
            indices=animal_subcategory_indices,
            table=AnimalSubcategory,
        )
        self.__create_index(
            indices=user_indices,
            table=User,
        )
        self.__create_index(
            indices=animal_indices,
            table=Animal,
        )
        self.__create_index(
            indices=like_indices,
            table=Like,
        )
        self.__create_index(
            indices=violation_type_indices,
            table=ViolationType,
        )
        self.__create_index(
            indices=violation_indices,
            table=Violation,
        )

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

    def __register_violation_type(
        self,
        file_path: str,
    ):
        logger.info(f"register violation type: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
        for k, v in data.items():
            request = ViolationTypeCreateRequest(
                id=k,
                name=v["name"],
            )
            self.violation_type_usecase.register(request=request)
        logger.info(f"done register violation type: {file_path}")

    def __register_user(
        self,
        file_path: str,
    ):
        logger.info(f"register user: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
        requests = []
        for k, v in data.items():
            requests.append(
                UserCreateRequest(
                    id=k,
                    handle_name=v["handle_name"],
                    email_address=v["email_address"],
                    password=v["password"],
                    age=v["age"],
                    gender=v["gender"],
                    created_at=datetime.strptime(v["created_at"], "%Y-%m-%dT%H:%M:%S.%f"),
                )
            )
        self.user_usecase.bulk_register(requests=requests)
        logger.info(f"done register user: {file_path}")

    def __register_animal(
        self,
        file_path: str,
    ):
        logger.info(f"register animal: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
        try:
            self.messaging.init_channel()
            self.messaging.create_queue(queue_name=Configurations.no_animal_violation_queue)
            self.messaging.channel.basic_qos(prefetch_count=1)
            requests = []
            for k, v in data.items():
                requests.append(
                    AnimalCreateRequest(
                        id=k,
                        animal_category_id=v["category"],
                        animal_subcategory_id=v["subcategory"],
                        user_id=v["user_id"],
                        name=v["name"],
                        description=v["description"],
                        photo_url=v["photo_url"],
                        created_at=datetime.strptime(v["created_at"], "%Y-%m-%dT%H:%M:%S.%f"),
                    )
                )
            self.animal_usecase.bulk_register(requests=requests)
        except Exception as e:
            logger.exception(e)
            raise e
        finally:
            self.messaging.close()
        logger.info(f"done register animal: {file_path}")

    def __register_violation(
        self,
        file_path: str,
    ):
        logger.info(f"register violation: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
        for k, v in data.items():
            request = ViolationCreateRequest(
                id=k,
                animal_id=v["animal_id"],
                violation_type_id=v["violation_type_id"],
                probability=v["probability"],
                judge=v["judge"],
                is_effective=v["is_effective"],
            )
            self.violation_usecase.register(request=request)
        logger.info(f"done register violation: {file_path}")

    def __register_access_log(
        self,
        file_path: str,
    ):
        logger.info(f"register access log: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
        requests = []
        for v in data["access_logs"]:
            requests.append(
                AccessLogCreateRequest(
                    id=v["id"],
                    phrases=v["phrases"],
                    animal_category_id=v["animal_category_id"],
                    animal_subcategory_id=v["animal_subcategory_id"],
                    user_id=v["user_id"],
                    likes=v["likes"],
                    animal_id=v["animal_id"],
                    action=v["action"],
                    created_at=datetime.strptime(v["created_at"], "%Y-%m-%d %H:%M:%S.%f"),
                )
            )
        self.access_log_usecase.bulk_register(requests=requests)
        logger.info(f"done register access_log: {file_path}")

    def run(self):
        logger.info("run initialize database")
        self.__create_table()
        self.__create_indices()
        self.__register_violation_type(file_path=Configurations.violation_type_file)
        self.__register_animal_category(file_path=Configurations.animal_category_file)
        self.__register_animal_subcategory(file_path=Configurations.animal_subcategory_file)
        self.__register_user(file_path=Configurations.user_file)
        self.__register_animal(file_path=Configurations.animal_file)
        self.__register_violation(file_path=Configurations.violation_file)
        self.__register_access_log(file_path=Configurations.access_log_file)
