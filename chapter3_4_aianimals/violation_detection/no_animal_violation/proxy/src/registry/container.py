import logging
import logging.config

from dependency_injector import containers, providers
from src.configurations import Configurations
from src.infrastructure.database import AbstractDatabase, PostgreSQLDatabase
from src.infrastructure.messaging import RabbitmqMessaging
from src.job.violation_detection_job import ViolationDetectionJob
from src.repository.animal_repository import AbstractAnimalRepository, AnimalRepository
from src.repository.violation_type_repository import AbstractViolationTypeRepository, ViolationTypeRepository
from src.service.predictor import AbstractPredictor, NoViolationDetectionPredictor


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()
    logging = providers.Resource(
        logging.config.fileConfig,
        fname=Configurations.logging_file,
    )


class Infrastructures(containers.DeclarativeContainer):
    config = providers.Configuration()

    database: AbstractDatabase = providers.Singleton(PostgreSQLDatabase())
    messaging: RabbitmqMessaging = providers.Singleton(RabbitmqMessaging())


class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration()
    infrastructures = providers.DependenciesContainer()

    animal_repository: AbstractAnimalRepository = providers.Factory(
        AnimalRepository,
        database=infrastructures.database,
    )
    violation_type_repository: AbstractViolationTypeRepository = providers.Factory(
        ViolationTypeRepository,
        database=infrastructures.database,
    )


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()

    no_violation_detection_predictor: AbstractPredictor = providers.Factory(
        NoViolationDetectionPredictor,
        url=Configurations.predictor_url,
        height=Configurations.predictor_height,
        width=Configurations.predictor_width,
    )


class Jobs(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = providers.DependenciesContainer()
    predictors = providers.DependenciesContainer()
    infrastructures = providers.DependenciesContainer()

    violation_detection_job: ViolationDetectionJob = providers.Factory(
        ViolationDetectionJob,
        messaging=infrastructures.messaging,
        violation_type_repository=repositories.violation_type_repository,
        animal_repository=repositories.animal_repository,
        predictor=predictors.no_violation_detection_predictor,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    core = providers.Container(Core)
    infrastructures = providers.Container(Infrastructures)
    repositories = providers.Container(
        Repositories,
        infrastructures=infrastructures,
    )
    services = providers.Container(Services)
    jobs = providers.Container(
        Jobs,
        repositories=repositories,
        services=services,
        infrastructures=infrastructures,
    )
