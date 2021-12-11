from src.job.abstract_job import AbstractJob
from src.middleware.logger import configure_logger
from src.usecase.animal_usecase import AbstractAnimalUsecase

logger = configure_logger(__name__)


class AnimalToSearchJob(AbstractJob):
    def __init__(
        self,
        animal_usecase: AbstractAnimalUsecase,
    ):
        super().__init__()
        self.animal_usecase = animal_usecase

    def _run(self):
        logger.info("register index...")
        while True:
            self.animal_usecase.register_index()

    def run(self):
        logger.info("run animal to search job")
        index_exists = self.animal_usecase.index_exists()
        if not index_exists:
            logger.info("register index")
            self.animal_usecase.create_index()

        self._run()
