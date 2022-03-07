from src.infrastructure.client.postgresql_database import PostgreSQLDatabase
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.infrastructure.database import AbstractDatabase
from src.job.violation_detection_job import ViolationDetectionJob
from src.middleware.logger import configure_logger
from src.service.predictor import AbstractPredictor, NoViolationDetectionPredictor
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.implementation.animal_repository import AnimalRepository
from src.repository.implementation.violation_type_repository import ViolationTypeRepository
from src.repository.violation_type_repository import AbstractViolationTypeRepository
from src.configurations import Configurations

logger = configure_logger(__name__)


class Container(object):
    def __init__(
        self,
        database: AbstractDatabase,
        messaging: RabbitmqMessaging,
        predictor: AbstractPredictor,
    ):
        self.database = database
        self.messaging = messaging
        self.predictor = predictor

        self.violation_type_repository: AbstractViolationTypeRepository = ViolationTypeRepository(
            database=self.database
        )
        self.animal_repository: AbstractAnimalRepository = AnimalRepository(database=self.database)

        self.violation_detection_job: ViolationDetectionJob = ViolationDetectionJob(
            messaging=self.messaging,
            violation_type_repository=self.violation_type_repository,
            animal_repository=self.animal_repository,
            predictor=self.predictor,
        )


container = Container(
    database=PostgreSQLDatabase(),
    messaging=RabbitmqMessaging(),
    predictor=NoViolationDetectionPredictor(
        url=Configurations.predictor_url,
        height=Configurations.predictor_height,
        width=Configurations.predictor_width,
    ),
)
