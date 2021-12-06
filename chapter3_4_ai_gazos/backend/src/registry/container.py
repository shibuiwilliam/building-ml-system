from logging import getLogger

from src.configurations import Configurations
from src.constants import RUN_ENVIRONMENT
from src.infrastructure.client.google_cloud_storage import GoogleCloudStorage
from src.infrastructure.client.local_storage import LocalStorage
from src.infrastructure.client.postgresql_database import PostgreSQLDatabase
from src.infrastructure.database import AbstractDatabase
from src.infrastructure.storage import AbstractStorage
from src.repository.content_repository import AbstractContentRepository
from src.repository.implementation.content_repository import ContentRepository
from src.repository.implementation.like_repository import LikeRepository
from src.repository.implementation.user_repository import UserRepository
from src.repository.like_repository import AbstractLikeRepository
from src.repository.user_repository import AbstractUserRepository
from src.usecase.content_usecase import AbstractContentUsecase
from src.usecase.implementation.content_usecase import ContentUsecase
from src.usecase.implementation.like_usecase import LikeUsecase
from src.usecase.implementation.metadata_usecase import MetadataUsecase
from src.usecase.implementation.user_usecase import UserUsecase
from src.usecase.like_usecase import AbstractLikeUsecase
from src.usecase.metadata_usecase import AbstractMetadataUsecase
from src.usecase.user_usecase import AbstractUserUsecase

logger = getLogger(__name__)


class Container(object):
    def __init__(
        self,
        storage_client: AbstractStorage,
        database: AbstractDatabase,
    ):
        self.database = database
        self.storage_client = storage_client
        self.content_reposigory: AbstractContentRepository = ContentRepository()
        self.user_repository: AbstractUserRepository = UserRepository()
        self.like_repository: AbstractLikeRepository = LikeRepository()

        self.user_usecase: AbstractUserUsecase = UserUsecase(
            user_repository=self.user_repository,
        )
        self.content_usecase: AbstractContentUsecase = ContentUsecase(
            like_repository=self.like_repository,
            user_repository=self.user_repository,
            content_repository=self.content_reposigory,
            storage_client=self.storage_client,
        )
        self.like_usecase: AbstractLikeUsecase = LikeUsecase(
            like_repository=self.like_repository,
        )
        self.metadata_usecase: AbstractMetadataUsecase = MetadataUsecase()


if Configurations.run_environment == RUN_ENVIRONMENT.LOCAL.value:
    storage_client: AbstractStorage = LocalStorage()
elif Configurations.run_environment == RUN_ENVIRONMENT.CLOUD.value:
    storage_client = GoogleCloudStorage()

container = Container(
    storage_client=storage_client,
    database=PostgreSQLDatabase(),
)
