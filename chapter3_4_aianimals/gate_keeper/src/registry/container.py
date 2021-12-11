from src.infrastructure.client.elastic_search import Elasticsearch
from src.infrastructure.client.postgresql_database import PostgreSQLDatabase
from src.infrastructure.client.redis_queue import RedisQueue
from src.infrastructure.database import AbstractDatabase
from src.infrastructure.queue import AbstractQueue
from src.infrastructure.search import AbstractSearch
from src.job.animal_to_search_job import AnimalToSearchJob
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.implementation.animal_repository import AnimalRepository
from src.usecase.animal_usecase import AbstractAnimalUsecase
from src.usecase.implementation.animal_usecase import AnimalUsecase

logger = configure_logger(__name__)


class Container(object):
    def __init__(
        self,
        database: AbstractDatabase,
        queue: AbstractQueue,
        search: AbstractSearch,
    ):
        self.database = database
        self.queue = queue
        self.search = search

        self.animal_reposigory: AbstractAnimalRepository = AnimalRepository(
            database=self.database,
            queue=self.queue,
            search=self.search,
        )
        self.animal_usecase: AbstractAnimalUsecase = AnimalUsecase(animal_repository=self.animal_reposigory)

        self.animal_search_job: AnimalToSearchJob = AnimalToSearchJob(animal_usecase=self.animal_usecase)


container = Container(
    database=PostgreSQLDatabase(),
    queue=RedisQueue(),
    search=Elasticsearch(),
)
