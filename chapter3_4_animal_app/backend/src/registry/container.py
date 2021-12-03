from logging import getLogger

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
from src.usecase.implementation.user_usecase import UserUsecase
from src.usecase.user_usecase import AbstractUserUsecase

logger = getLogger(__name__)


class Container(object):
    def __init__(
        self,
        animal_category_usecase: AbstractAnimalCategoryUsecase,
        animal_subcategory_usecase: AbstractAnimalSubcategoryUsecase,
        user_usecase: AbstractUserUsecase,
        animal_usecase: AbstractAnimalUsecase,
    ):
        self.animal_category_usecase = animal_category_usecase
        self.animal_subcategory_usecase = animal_subcategory_usecase
        self.user_usecase = user_usecase
        self.animal_usecase = animal_usecase


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
    ),
)
