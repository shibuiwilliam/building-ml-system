import logging.config

from dependency_injector import containers, providers
from src.configurations import Configurations
from src.infrastructure.database import AbstractDatabase, PostgreSQLDatabase
from src.infrastructure.messaging import RabbitmqMessaging
from src.job.register_violation_job import RegisterViolationJob
from src.repository.animal_repository import AbstractAnimalRepository, AnimalRepository
from src.repository.violation_repository import AbstractViolationRepository, ViolationRepository
from src.repository.violation_type_repository import AbstractViolationTypeRepository, ViolationTypeRepository
from src.usecase.violation_usecase import AbstractViolationUsecase, ViolationUsecase


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
    violation_repository: AbstractViolationRepository = providers.Factory(
        ViolationRepository,
        database=infrastructures.database,
    )


class Usecases(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = providers.DependenciesContainer()

    violation_usecase: AbstractViolationUsecase = providers.Factory(
        ViolationUsecase,
        violation_repository=repositories.violation_repository,
        violation_type_repository=repositories.violation_type_repository,
        animal_repository=repositories.animal_repository,
    )


class Jobs(containers.DeclarativeContainer):
    config = providers.Configuration()
    usecases = providers.DependenciesContainer()
    infrastructures = providers.DependenciesContainer()

    register_violation_job: RegisterViolationJob = providers.Factory(
        RegisterViolationJob,
        violation_usecase=usecases.violation_usecase,
        messaging=infrastructures.messaging,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    core = providers.Container(Core)
    infrastructures = providers.Container(Infrastructures)
    repositories = providers.Container(
        Repositories,
        infrastructures=infrastructures,
    )
    usecases = providers.Container(
        Usecases,
        repositories=repositories,
    )
    jobs = providers.Container(
        Jobs,
        usecases=usecases,
        infrastructures=infrastructures,
    )
