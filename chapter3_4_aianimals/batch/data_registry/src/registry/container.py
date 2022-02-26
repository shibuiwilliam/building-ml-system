from src.configurations import Configurations
from src.infrastructure.client.elastic_search import Elasticsearch
from src.infrastructure.client.postgresql_database import PostgreSQLDatabase
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.infrastructure.database import AbstractDatabase
from src.infrastructure.search import AbstractSearch
from src.job.animal_feature_registration_job import AnimalFeatureRegistrationJob
from src.job.animal_to_search_job import AnimalToSearchJob
from src.job.initialization_job import InitializationJob
from src.middleware.logger import configure_logger
from src.repository.access_log_repository import AbstractAccessLogRepository, AccessLogRepository
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository, AnimalCategoryRepository
from src.repository.animal_feature_repository import AbstractAnimalFeatureRepository, AnimalFeatureRepository
from src.repository.animal_repository import AbstractAnimalRepository, AnimalRepository
from src.repository.animal_subcategory_repository import (
    AbstractAnimalSubcategoryRepository,
    AnimalSubcategoryRepository,
)
from src.repository.like_repository import AbstractLikeRepository, LikeRepository
from src.repository.table_repository import AbstractTableRepository, TableRepository
from src.repository.user_repository import AbstractUserRepository, UserRepository
from src.repository.violation_repository import AbstractViolationRepository, ViolationRepository
from src.repository.violation_type_repository import AbstractViolationTypeRepository, ViolationTypeRepository
from src.service.text_processing import DescriptionTokenizer, DescriptionVectorizer, NameTokenizer, NameVectorizer
from src.usecase.access_log_usecase import AbstractAccessLogUsecase, AccessLogUsecase
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase, AnimalCategoryUsecase
from src.usecase.animal_subcategory_usecase import AbstractAnimalSubcategoryUsecase, AnimalSubcategoryUsecase
from src.usecase.animal_usecase import AbstractAnimalUsecase, AnimalUsecase
from src.usecase.like_usecase import AbstractLikeUsecase, LikeUsecase
from src.usecase.table_usecase import AbstractTableUsecase, TableUsecase
from src.usecase.user_usecase import AbstractUserUsecase, UserUsecase
from src.usecase.violation_type_usecase import AbstractViolationTypeUsecase, ViolationTypeUsecase
from src.usecase.violation_usecase import AbstractViolationUsecase, ViolationUsecase

logger = configure_logger(__name__)


class Container(object):
    def __init__(
        self,
        database: AbstractDatabase,
        messaging: RabbitmqMessaging,
        search: AbstractSearch,
        description_tokenizer: DescriptionTokenizer,
        name_tokenizer: NameTokenizer,
        description_vectorizer: DescriptionVectorizer,
        name_vectorizer: NameVectorizer,
    ):
        self.database = database
        self.search = search
        self.messaging = messaging
        self.messaging.init_channel()
        for q in Configurations.animal_violation_queues:
            self.messaging.create_queue(queue_name=q)
        self.messaging.create_queue(queue_name=Configurations.animal_registry_queue)
        self.messaging.create_queue(queue_name=Configurations.animal_feature_registry_queue)

        self.description_tokenizer = description_tokenizer
        self.name_tokenizer = name_tokenizer
        self.description_vectorizer = description_vectorizer
        self.name_vectorizer = name_vectorizer

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
        self.violation_repository: AbstractViolationRepository = ViolationRepository(database=self.database)
        self.access_log_repository: AbstractAccessLogRepository = AccessLogRepository(database=self.database)
        self.animal_feature_repository: AbstractAnimalFeatureRepository = AnimalFeatureRepository(
            database=self.database
        )

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
            animal_feature_repository=self.animal_feature_repository,
            messaging=self.messaging,
            search=self.search,
            description_tokenizer=self.description_tokenizer,
            name_tokenizer=self.name_tokenizer,
            description_vectorizer=self.description_vectorizer,
            name_vectorizer=self.name_vectorizer,
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
        self.animal_search_job: AnimalToSearchJob = AnimalToSearchJob(
            animal_usecase=self.animal_usecase,
            messaging=self.messaging,
        )
        self.animal_feature_registration_job: AnimalFeatureRegistrationJob = AnimalFeatureRegistrationJob(
            animal_usecase=self.animal_usecase,
            messaging=self.messaging,
        )


container = Container(
    database=PostgreSQLDatabase(),
    search=Elasticsearch(),
    messaging=RabbitmqMessaging(),
    description_tokenizer=DescriptionTokenizer(),
    name_tokenizer=NameTokenizer(),
    description_vectorizer=DescriptionVectorizer(),
    name_vectorizer=NameVectorizer(),
)
