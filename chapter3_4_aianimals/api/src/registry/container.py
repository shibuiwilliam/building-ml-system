from logging import getLogger

from src.configurations import Configurations
from src.constants import RUN_ENVIRONMENT
from src.infrastructure.cache import AbstractCache, RedisCache
from src.infrastructure.database import AbstractDatabase, PostgreSQLDatabase
from src.infrastructure.messaging import AbstractMessaging, RabbitmqMessaging
from src.infrastructure.search import AbstractSearch, ElasticsearchClient
from src.infrastructure.storage import AbstractStorage, GoogleCloudStorage, LocalStorage
from src.middleware.crypt import AbstractCrypt, Crypt
from src.repository.access_log_repository import AbstractAccessLogRepository, AccessLogRepository
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository, AnimalCategoryRepository
from src.repository.animal_repository import AbstractAnimalRepository, AnimalRepository
from src.repository.animal_subcategory_repository import (
    AbstractAnimalSubcategoryRepository,
    AnimalSubcategoryRepository,
)
from src.repository.like_repository import AbstractLikeRepository, LikeRepository
from src.repository.user_repository import AbstractUserRepository, UserRepository
from src.repository.violation_repository import AbstractViolationRepository, ViolationRepository
from src.repository.violation_type_repository import AbstractViolationTypeRepository, ViolationTypeRepository
from src.usecase.access_log_usecase import AbstractAccessLogUsecase, AccessLogUsecase
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase, AnimalCategoryUsecase
from src.usecase.animal_subcategory_usecase import AbstractAnimalSubcategoryUsecase, AnimalSubcategoryUsecase
from src.usecase.animal_usecase import AbstractAnimalUsecase, AnimalUsecase
from src.usecase.like_usecase import AbstractLikeUsecase, LikeUsecase
from src.usecase.metadata_usecase import AbstractMetadataUsecase, MetadataUsecase
from src.usecase.user_usecase import AbstractUserUsecase, UserUsecase
from src.usecase.violation_type_usecase import AbstractViolationTypeUsecase, ViolationTypeUsecase
from src.usecase.violation_usecase import AbstractViolationUsecase, ViolationUsecase

logger = getLogger(__name__)


class Container(object):
    def __init__(
        self,
        storage_client: AbstractStorage,
        database: AbstractDatabase,
        cache: AbstractCache,
        search_client: AbstractSearch,
        messaging: AbstractMessaging,
        crypt: AbstractCrypt,
    ):
        self.database = database
        self.storage_client = storage_client
        self.cache = cache
        self.search_client = search_client
        self.messaging = messaging
        self.messaging.init_channel()
        for q in Configurations.animal_violation_queues:
            self.messaging.create_queue(queue_name=q)
        self.crypt = crypt

        self.animal_category_repository: AbstractAnimalCategoryRepository = AnimalCategoryRepository()
        self.animal_subcategory_repository: AbstractAnimalSubcategoryRepository = AnimalSubcategoryRepository()
        self.animal_repository: AbstractAnimalRepository = AnimalRepository()
        self.user_repository: AbstractUserRepository = UserRepository()
        self.like_repository: AbstractLikeRepository = LikeRepository()
        self.violation_type_repository: AbstractViolationTypeRepository = ViolationTypeRepository()
        self.violation_repository: AbstractViolationRepository = ViolationRepository()
        self.access_log_repository: AbstractAccessLogRepository = AccessLogRepository()

        self.animal_category_usecase: AbstractAnimalCategoryUsecase = AnimalCategoryUsecase(
            animal_category_repository=self.animal_category_repository,
        )
        self.animal_subcategory_usecase: AbstractAnimalSubcategoryUsecase = AnimalSubcategoryUsecase(
            animal_category_repository=self.animal_category_repository,
            animal_subcategory_repository=self.animal_subcategory_repository,
        )
        self.user_usecase: AbstractUserUsecase = UserUsecase(
            user_repository=self.user_repository,
            crypt=self.crypt,
        )
        self.animal_usecase: AbstractAnimalUsecase = AnimalUsecase(
            animal_repository=self.animal_repository,
            like_repository=self.like_repository,
            storage_client=self.storage_client,
            cache=self.cache,
            search_client=self.search_client,
            messaging=self.messaging,
        )
        self.like_usecase: AbstractLikeUsecase = LikeUsecase(
            like_repository=self.like_repository,
            cache=self.cache,
        )
        self.violation_type_usecase: AbstractViolationTypeUsecase = ViolationTypeUsecase(
            violation_type_repository=self.violation_type_repository
        )
        self.violation_usecase: AbstractViolationUsecase = ViolationUsecase(
            violation_repository=self.violation_repository
        )
        self.access_log_usecase: AbstractAccessLogUsecase = AccessLogUsecase(
            access_log_repository=self.access_log_repository,
            like_repository=self.like_repository,
        )
        self.metadata_usecase: AbstractMetadataUsecase = MetadataUsecase(
            animal_category_repository=self.animal_category_repository,
            animal_subcategory_repository=self.animal_subcategory_repository,
        )


if Configurations.run_environment == RUN_ENVIRONMENT.LOCAL.value:
    storage_client: AbstractStorage = LocalStorage()
elif Configurations.run_environment == RUN_ENVIRONMENT.CLOUD.value:
    storage_client = GoogleCloudStorage()

container = Container(
    storage_client=storage_client,
    database=PostgreSQLDatabase(),
    cache=RedisCache(),
    search_client=ElasticsearchClient(),
    messaging=RabbitmqMessaging(),
    crypt=Crypt(key_file_path=Configurations.key_file_path),
)
