from logging import getLogger

from src.configurations import Configurations
from src.constants import RUN_ENVIRONMENT
from src.infrastructure.client.google_cloud_storage import GoogleCloudStorage
from src.infrastructure.client.local_storage import LocalStorage
from src.infrastructure.client.postgresql_database import PostgreSQLDatabase
from src.infrastructure.database import AbstractDatabase
from src.infrastructure.storage import AbstractStorage
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository
from src.repository.implementation.animal_category_repository import AnimalCategoryRepository
from src.repository.implementation.animal_repository import AnimalRepository
from src.repository.implementation.animal_subcategory_repository import AnimalSubcategoryRepository
from src.repository.implementation.like_repository import LikeRepository
from src.repository.implementation.user_repository import UserRepository
from src.repository.like_repository import AbstractLikeRepository
from src.repository.user_repository import AbstractUserRepository
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase
from src.usecase.animal_subcategory_usecase import AbstractAnimalSubcategoryUsecase
from src.usecase.animal_usecase import AbstractAnimalUsecase
from src.usecase.implementation.animal_category_usecase import AnimalCategoryUsecase
from src.usecase.implementation.animal_subcategory_usecase import AnimalSubcategoryUsecase
from src.usecase.implementation.animal_usecase import AnimalUsecase
from src.usecase.implementation.like_usecase import LikeUsecase
from src.usecase.implementation.user_usecase import UserUsecase
from src.usecase.like_usecase import AbstractLikeUsecase
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

        self.animal_category_repository: AbstractAnimalCategoryRepository = AnimalCategoryRepository()
        self.animal_subcategory_repository: AbstractAnimalSubcategoryRepository = AnimalSubcategoryRepository()
        self.animal_reposigory: AbstractAnimalRepository = AnimalRepository()
        self.user_repository: AbstractUserRepository = UserRepository()
        self.like_repository: AbstractLikeRepository = LikeRepository()

        self.animal_category_usecase: AbstractAnimalCategoryUsecase = AnimalCategoryUsecase(
            animal_category_repository=self.animal_category_repository,
        )
        self.animal_subcategory_usecase: AbstractAnimalSubcategoryUsecase = AnimalSubcategoryUsecase(
            animal_category_repository=self.animal_category_repository,
            animal_subcategory_repository=self.animal_subcategory_repository,
        )
        self.user_usecase: AbstractUserUsecase = UserUsecase(
            user_repository=self.user_repository,
        )
        self.animal_usecase: AbstractAnimalUsecase = AnimalUsecase(
            like_repository=self.like_repository,
            user_repository=self.user_repository,
            animal_category_repository=self.animal_category_repository,
            animal_subcategory_repository=self.animal_subcategory_repository,
            animal_repository=self.animal_reposigory,
            storage_client=self.storage_client,
        )
        self.like_usecase: AbstractLikeUsecase = LikeUsecase(
            like_repository=self.like_repository,
        )


if Configurations.run_environment == RUN_ENVIRONMENT.LOCAL.value:
    storage_client: AbstractStorage = LocalStorage()
elif Configurations.run_environment == RUN_ENVIRONMENT.LOCAL.value:
    storage_client = GoogleCloudStorage()

container = Container(
    storage_client=storage_client,
    database=PostgreSQLDatabase(),
)
