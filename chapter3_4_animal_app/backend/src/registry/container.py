from logging import getLogger

from src.repository.implementation.animal_category_repository import AnimalCategoryRepository
from src.repository.implementation.animal_subcategory_repository import AnimalSubcategoryRepository
from src.repository.implementation.user_repository import UserRepository
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase
from src.usecase.animal_subcategory_usecase import AbstractAnimalSubcategoryUsecase
from src.usecase.implementation.animal_category_usecase import AnimalCategoryUsecase
from src.usecase.implementation.animal_subcategory_usecase import AnimalSubcategoryUsecase
from src.usecase.implementation.user_usecase import UserUsecase
from src.usecase.user_usecase import AbstractUserUsecase

logger = getLogger(__name__)


class Container(object):
    def __init__(
        self,
        animal_category_usecase: AbstractAnimalCategoryUsecase,
        animal_subcategory_usecase: AbstractAnimalSubcategoryUsecase,
        user_usecase: AbstractUserUsecase,
    ):
        self.animal_category_usecase = animal_category_usecase
        self.animal_subcategory_usecase = animal_subcategory_usecase
        self.user_usecase = user_usecase


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
)
