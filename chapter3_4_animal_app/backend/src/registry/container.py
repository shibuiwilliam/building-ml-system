from logging import getLogger

from src.repository.animal_category_repository import AnimalCategoryRepository
from src.repository.animal_repository import AnimalRepository
from src.repository.animal_subcategory_repository import AnimalSubcategoryRepository
from src.repository.user_repository import UserRepository
from src.usecase.animal_category_usecase import AnimalCategoryUsecase
from src.usecase.animal_subcategory_usecase import AnimalSubcategoryUsecase
from src.usecase.animal_usecase import AnimalUsecase
from src.usecase.user_usecase import UserUsecase

logger = getLogger(__name__)


class Container(object):
    def __init__(self):
        self.animal_category_repository = AnimalCategoryRepository()
        self.animal_subcategory_repository = AnimalSubcategoryRepository()
        self.user_repository = UserRepository()
        self.animal_repository = AnimalRepository()

        self.animal_category_usecase = AnimalCategoryUsecase(animal_category_repository=self.animal_category_repository)
        self.animal_subcategory_usecase = AnimalSubcategoryUsecase(
            animal_subcategory_repository=self.animal_subcategory_repository,
            animal_category_repository=self.animal_category_repository,
        )
        self.user_usecase = UserUsecase(user_repository=self.user_repository)
        self.animal_usecase = AnimalUsecase(
            animal_repository=self.animal_repository,
            animal_subcategory_repository=self.animal_subcategory_repository,
            animal_category_repository=self.animal_category_repository,
        )


container = Container()
