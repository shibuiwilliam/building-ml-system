from src.controller.animal_category_controller import AbstractAnimalCategoryController
from src.controller.animal_controller import AbstractAnimalController
from src.controller.animal_subcategory_controller import AbstractAnimalSubcategoryController
from src.controller.implementation.animal_category_controller import AnimalCategoryController
from src.controller.implementation.animal_controller import AnimalController
from src.controller.implementation.animal_subcategory_controller import AnimalSubcategoryController
from src.controller.implementation.like_controller import LikeController
from src.controller.implementation.table_controller import TableController
from src.controller.implementation.user_controller import UserController
from src.controller.like_controller import AbstractLikeController
from src.controller.table_controller import AbstractTableController
from src.controller.user_controller import AbstractUserController
from src.infrastructure.client.postgresql_database import PostgreSQLDatabase
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository
from src.repository.implementation.animal_category_repository import AnimalCategoryRepository
from src.repository.implementation.animal_repository import AnimalRepository
from src.repository.implementation.animal_subcategory_repository import AnimalSubcategoryRepository
from src.repository.implementation.like_repository import LikeRepository
from src.repository.implementation.table_repository import TableRepository
from src.repository.implementation.user_repository import UserRepository
from src.repository.like_repository import AbstractLikeRepository
from src.repository.table_repository import AbstractTableRepository
from src.repository.user_repository import AbstractUserRepository
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase
from src.usecase.animal_subcategory_usecase import AbstractAnimalSubcategoryUsecase
from src.usecase.animal_usecase import AbstractAnimalUsecase
from src.usecase.implementation.animal_category_usecase import AnimalCategoryUsecase
from src.usecase.implementation.animal_subcategory_usecase import AnimalSubcategoryUsecase
from src.usecase.implementation.animal_usecase import AnimalUsecase
from src.usecase.implementation.like_usecase import LikeUsecase
from src.usecase.implementation.table_usecase import TableUsecase
from src.usecase.implementation.user_usecase import UserUsecase
from src.usecase.like_usecase import AbstractLikeUsecase
from src.usecase.table_usecase import AbstractTableUsecase
from src.usecase.user_usecase import AbstractUserUsecase

logger = configure_logger(__name__)


class Container(object):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.database = database

        self.table_repository: AbstractTableRepository = TableRepository()
        self.animal_category_repository: AbstractAnimalCategoryRepository = AnimalCategoryRepository()
        self.animal_subcategory_repository: AbstractAnimalSubcategoryRepository = AnimalSubcategoryRepository()
        self.animal_reposigory: AbstractAnimalRepository = AnimalRepository()
        self.user_repository: AbstractUserRepository = UserRepository()
        self.like_repository: AbstractLikeRepository = LikeRepository()

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
        self.animal_usecase: AbstractAnimalUsecase = AnimalUsecase(animal_repository=self.animal_reposigory)
        self.like_usecase: AbstractLikeUsecase = LikeUsecase(
            like_repository=self.like_repository,
        )

        self.table_controller: AbstractTableController = TableController(table_usecase=self.table_usecase)
        self.animal_category_controller: AbstractAnimalCategoryController = AnimalCategoryController(
            animal_category_usecase=self.animal_category_usecase
        )
        self.animal_subcategory_controller: AbstractAnimalSubcategoryController = AnimalSubcategoryController(
            animal_subcategory_usecase=self.animal_subcategory_usecase
        )
        self.user_controller: AbstractUserController = UserController(user_usecase=self.user_usecase)
        self.animal_controller: AbstractAnimalController = AnimalController(animal_usecase=self.animal_usecase)
        self.like_controller: AbstractLikeController = LikeController(like_usecase=self.like_usecase)


container = Container(
    database=PostgreSQLDatabase(),
)
