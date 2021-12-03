from logging import getLogger

from src.configurations import Configurations
from src.constants import RUN_ENVIRONMENT
from src.infrastructure.client.google_cloud_storage import GoogleCloudStorage
from src.infrastructure.client.local_storage import LocalStorage
from src.infrastructure.client.postgresql_database import PostgreSQLDatabase
from src.infrastructure.database import AbstractDatabase
from src.infrastructure.storage import AbstractStorage
from src.repository.implementation.animal_category_repository import AnimalCategoryRepository
from src.repository.implementation.animal_repository import AnimalRepository
from src.repository.implementation.animal_subcategory_repository import AnimalSubcategoryRepository
from src.repository.implementation.like_repository import LikeRepository
from src.repository.implementation.user_repository import UserRepository
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
        animal_category_usecase: AbstractAnimalCategoryUsecase,
        animal_subcategory_usecase: AbstractAnimalSubcategoryUsecase,
        user_usecase: AbstractUserUsecase,
        animal_usecase: AbstractAnimalUsecase,
        like_usecase: AbstractLikeUsecase,
        database: AbstractDatabase,
    ):
        self.animal_category_usecase = animal_category_usecase
        self.animal_subcategory_usecase = animal_subcategory_usecase
        self.user_usecase = user_usecase
        self.animal_usecase = animal_usecase
        self.like_usecase = like_usecase
        self.database = database


if Configurations.run_environment == RUN_ENVIRONMENT.LOCAL.value:
    storage_client: AbstractStorage = LocalStorage()
elif Configurations.run_environment == RUN_ENVIRONMENT.LOCAL.value:
    storage_client = GoogleCloudStorage()

container = Container(
    animal_category_usecase=AnimalCategoryUsecase(
        animal_category_repository=AnimalCategoryRepository(),
    ),
    animal_subcategory_usecase=AnimalSubcategoryUsecase(
        animal_category_repository=AnimalCategoryRepository(),
        animal_subcategory_repository=AnimalSubcategoryRepository(),
    ),
    user_usecase=UserUsecase(
        user_repository=UserRepository(),
    ),
    animal_usecase=AnimalUsecase(
        like_repository=LikeRepository(),
        user_repository=UserRepository(),
        animal_category_repository=AnimalCategoryRepository(),
        animal_subcategory_repository=AnimalSubcategoryRepository(),
        animal_repository=AnimalRepository(),
        storage_client=storage_client,
    ),
    like_usecase=LikeUsecase(
        like_repository=LikeRepository(),
    ),
    database=PostgreSQLDatabase(),
)
