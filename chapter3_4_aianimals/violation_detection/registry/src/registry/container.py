from src.infrastructure.client.postgresql_database import PostgreSQLDatabase
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.infrastructure.database import AbstractDatabase
from src.infrastructure.messaging import AbstractMessaging
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.implementation.animal_repository import AnimalRepository
from src.repository.implementation.violation_repository import ViolationRepository
from src.repository.implementation.violation_type_repository import ViolationTypeRepository
from src.repository.violation_repository import AbstractViolationRepository
from src.repository.violation_type_repository import AbstractViolationTypeRepository
from src.usecase.implementation.violation_usecase import ViolationUsecase
from src.usecase.violation_usecase import AbstractViolationUsecase

logger = configure_logger(__name__)


class Container(object):
    def __init__(
        self,
        database: AbstractDatabase,
        messaging: AbstractMessaging,
    ):
        self.database = database
        self.messaging = messaging

        self.animal_repository: AbstractAnimalRepository = AnimalRepository(database=self.database)
        self.violation_type_repository: AbstractViolationTypeRepository = ViolationTypeRepository(
            database=self.database
        )
        self.violation_repository: AbstractViolationRepository = ViolationRepository(database=database)

        self.violation_usecase: AbstractViolationUsecase = ViolationUsecase(
            violation_repository=self.violation_repository,
            violation_type_repository=self.violation_type_repository,
            animal_repository=self.animal_repository,
        )


container = Container(
    database=PostgreSQLDatabase(),
    messaging=RabbitmqMessaging(),
)
