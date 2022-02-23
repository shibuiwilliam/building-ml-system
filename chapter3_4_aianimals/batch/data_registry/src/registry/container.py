from src.configurations import Configurations
from src.infrastructure.client.elastic_search import Elasticsearch
from src.infrastructure.client.postgresql_database import PostgreSQLDatabase
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.infrastructure.database import AbstractDatabase
from src.infrastructure.search import AbstractSearch
from src.job.animal_to_search_job import AnimalToSearchJob
from src.job.initialization_job import InitializationJob
from src.middleware.logger import configure_logger
from src.repository.access_log_repository import AbstractAccessLogRepository
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository
from src.repository.implementation.access_log_repository import AccessLogRepository
from src.repository.implementation.animal_category_repository import AnimalCategoryRepository
from src.repository.implementation.animal_repository import AnimalRepository
from src.repository.implementation.animal_subcategory_repository import AnimalSubcategoryRepository
from src.repository.implementation.like_repository import LikeRepository
from src.repository.implementation.table_repository import TableRepository
from src.repository.implementation.user_repository import UserRepository
from src.repository.implementation.violation_repository import ViolationRepository
from src.repository.implementation.violation_type_repository import ViolationTypeRepository
from src.repository.like_repository import AbstractLikeRepository
from src.repository.table_repository import AbstractTableRepository
from src.repository.user_repository import AbstractUserRepository
from src.repository.violation_repository import AbstractViolationRepository
from src.repository.violation_type_repository import AbstractViolationTypeRepository
from src.usecase.access_log_usecase import AbstractAccessLogUsecase
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase
from src.usecase.animal_subcategory_usecase import AbstractAnimalSubcategoryUsecase
from src.usecase.animal_usecase import AbstractAnimalUsecase
from src.usecase.implementation.access_log_usecase import AccessLogUsecase
from src.usecase.implementation.animal_category_usecase import AnimalCategoryUsecase
from src.usecase.implementation.animal_subcategory_usecase import AnimalSubcategoryUsecase
from src.usecase.implementation.animal_usecase import AnimalUsecase
from src.usecase.implementation.like_usecase import LikeUsecase
from src.usecase.implementation.table_usecase import TableUsecase
from src.usecase.implementation.user_usecase import UserUsecase
from src.usecase.implementation.violation_type_usecase import ViolationTypeUsecase
from src.usecase.implementation.violation_usecase import ViolationUsecase
from src.usecase.like_usecase import AbstractLikeUsecase
from src.usecase.table_usecase import AbstractTableUsecase
from src.usecase.user_usecase import AbstractUserUsecase
from src.usecase.violation_type_usecase import AbstractViolationTypeUsecase
from src.usecase.violation_usecase import AbstractViolationUsecase

logger = configure_logger(__name__)


class Container(object):
    def __init__(
        self,
        database: AbstractDatabase,
        messaging: RabbitmqMessaging,
        search: AbstractSearch,
    ):
        self.database = database
        self.search = search
        self.messaging = messaging
        self.messaging.init_channel()
        for q in Configurations.animal_violation_queues:
            self.messaging.create_queue(queue_name=q)

        self.table_repository: AbstractTableRepository = TableRepository()
        self.animal_category_repository: AbstractAnimalCategoryRepository = AnimalCategoryRepository(
            database=self.database
        )
        self.animal_subcategory_repository: AbstractAnimalSubcategoryRepository = AnimalSubcategoryRepository(
            database=self.database
        )
        self.animal_repository: AbstractAnimalRepository = AnimalRepository(database=self.database)
        self.user_repository: AbstractUserRepository = UserRepository(database=self.database)
        self.like_repository: AbstractLikeRepository = LikeRepository(database=self.database)
        self.violation_type_repository: AbstractViolationTypeRepository = ViolationTypeRepository(
            database=self.database
        )
        self.violation_repository: AbstractViolationRepository = ViolationRepository(database=database)
        self.access_log_repository: AbstractAccessLogRepository = AccessLogRepository(database=database)

        self.table_usecase: AbstractTableUsecase = TableUsecase(table_repository=self.table_repository)
        self.animal_category_usecase: AbstractAnimalCategoryUsecase = AnimalCategoryUsecase(
            animal_category_repository=self.animal_category_repository,
        )
        self.animal_subcategory_usecase: AbstractAnimalSubcategoryUsecase = AnimalSubcategoryUsecase(
            animal_subcategory_repository=self.animal_subcategory_repository,
        )
        self.user_usecase: AbstractUserUsecase = UserUsecase(
            user_repository=self.user_repository,
        )
        self.animal_usecase: AbstractAnimalUsecase = AnimalUsecase(
            animal_repository=self.animal_repository,
            like_repository=self.like_repository,
            messaging=self.messaging,
            search=self.search,
        )
        self.like_usecase: AbstractLikeUsecase = LikeUsecase(
            like_repository=self.like_repository,
        )
        self.violation_type_usecase: AbstractViolationTypeUsecase = ViolationTypeUsecase(
            violation_type_repository=self.violation_type_repository
        )
        self.violation_usecase: AbstractViolationUsecase = ViolationUsecase(
            violation_repository=self.violation_repository,
            animal_repository=self.animal_repository,
        )
        self.access_log_usecase: AbstractAccessLogUsecase = AccessLogUsecase(
            access_log_repository=self.access_log_repository
        )

        self.animal_search_job: AnimalToSearchJob = AnimalToSearchJob(
            animal_usecase=self.animal_usecase,
            messaging=self.messaging,
        )
        self.initialization_job: InitializationJob = InitializationJob(
            table_usecase=self.table_usecase,
            animal_category_usecase=self.animal_category_usecase,
            animal_subcategory_usecase=self.animal_subcategory_usecase,
            user_usecase=self.user_usecase,
            animal_usecase=self.animal_usecase,
            violation_type_usecase=self.violation_type_usecase,
            violation_usecase=self.violation_usecase,
            access_log_usecase=self.access_log_usecase,
            messaging=self.messaging,
            engine=self.database.engine,
        )


container = Container(
    database=PostgreSQLDatabase(),
    search=Elasticsearch(),
    messaging=RabbitmqMessaging(),
)
