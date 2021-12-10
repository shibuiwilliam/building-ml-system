from concurrent.futures import ThreadPoolExecutor

from src.controller.animal_controller import AbstractAnimalController
from src.middleware.logger import configure_logger
from src.usecase.animal_usecase import AbstractAnimalUsecase

logger = configure_logger(__name__)


class AnimalController(AbstractAnimalController):
    def __init__(
        self,
        animal_usecase: AbstractAnimalUsecase,
    ):
        super().__init__(animal_usecase=animal_usecase)

    def run(self):
        index_exists = self.animal_usecase.get_index()
        if index_exists is None or len(index_exists) == 0:
            self.animal_usecase.create_index()

        while True:
            with ThreadPoolExecutor(4) as executor:
                executor.map(self.animal_usecase.register_index)
