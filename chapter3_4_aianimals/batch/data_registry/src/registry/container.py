import logging.config

from dependency_injector import containers, providers
from src.configurations import Configurations
from src.infrastructure.cache import AbstractCache, RedisCache
from src.infrastructure.database import AbstractDatabase, PostgreSQLDatabase
from src.infrastructure.messaging import RabbitmqMessaging
from src.infrastructure.search import AbstractSearch, ElasticsearchClient
from src.job.animal_to_search_job import AnimalToSearchJob
from src.job.initialization_job import InitializationJob
from src.repository.access_log_repository import AbstractAccessLogRepository, AccessLogRepository
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository, AnimalCategoryRepository
from src.repository.animal_repository import AbstractAnimalRepository, AnimalRepository
from src.repository.animal_subcategory_repository import (
    AbstractAnimalSubcategoryRepository,
    AnimalSubcategoryRepository,
)
from src.repository.like_repository import AbstractLikeRepository, LikeRepository
from src.repository.table_repository import AbstractTableRepository, TableRepository
from src.repository.user_repository import AbstractUserRepository, UserRepository
from src.repository.violation_repository import AbstractViolationRepository, ViolationRepository
from src.repository.violation_type_repository import AbstractViolationTypeRepository, ViolationTypeRepository
from src.usecase.access_log_usecase import AbstractAccessLogUsecase, AccessLogUsecase
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase, AnimalCategoryUsecase
from src.usecase.animal_subcategory_usecase import AbstractAnimalSubcategoryUsecase, AnimalSubcategoryUsecase
from src.usecase.animal_usecase import AbstractAnimalUsecase, AnimalUsecase
from src.usecase.like_usecase import AbstractLikeUsecase, LikeUsecase
from src.usecase.table_usecase import AbstractTableUsecase, TableUsecase
from src.usecase.user_usecase import AbstractUserUsecase, UserUsecase
from src.usecase.violation_type_usecase import AbstractViolationTypeUsecase, ViolationTypeUsecase
from src.usecase.violation_usecase import AbstractViolationUsecase, ViolationUsecase


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()
    logging = providers.Resource(
        logging.config.fileConfig,
        fname=Configurations.logging_file,
    )


class Infrastructures(containers.DeclarativeContainer):
    config = providers.Configuration()

    database: AbstractDatabase = providers.Singleton(PostgreSQLDatabase)
    messaging: RabbitmqMessaging = providers.Singleton(RabbitmqMessaging)
    search: AbstractSearch = providers.Singleton(ElasticsearchClient)
    cache: AbstractCache = providers.Singleton(RedisCache)


class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration()
    infrastructures = providers.DependenciesContainer()

    table_repository: AbstractTableRepository = providers.Factory(TableRepository)
    animal_category_repository: AbstractAnimalCategoryRepository = providers.Factory(
        AnimalCategoryRepository,
        database=infrastructures.database,
    )
    animal_subcategory_repository: AbstractAnimalSubcategoryRepository = providers.Factory(
        AnimalSubcategoryRepository,
        database=infrastructures.database,
    )
    animal_repository: AbstractAnimalRepository = providers.Factory(
        AnimalRepository,
        database=infrastructures.database,
    )
    user_repository: AbstractUserRepository = providers.Factory(
        UserRepository,
        database=infrastructures.database,
    )
    like_repository: AbstractLikeRepository = providers.Factory(
        LikeRepository,
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
    access_log_repository: AbstractAccessLogRepository = providers.Factory(
        AccessLogRepository,
        database=infrastructures.database,
    )


class Usecases(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = providers.DependenciesContainer()
    infrastructures = providers.DependenciesContainer()

    table_usecase: AbstractTableUsecase = providers.Factory(
        TableUsecase,
        table_repository=repositories.table_repository,
    )
    animal_category_usecase: AbstractAnimalCategoryUsecase = providers.Factory(
        AnimalCategoryUsecase,
        animal_category_repository=repositories.animal_category_repository,
    )
    animal_subcategory_usecase: AbstractAnimalSubcategoryUsecase = providers.Factory(
        AnimalSubcategoryUsecase,
        animal_subcategory_repository=repositories.animal_subcategory_repository,
    )
    user_usecase: AbstractUserUsecase = providers.Factory(
        UserUsecase,
        user_repository=repositories.user_repository,
    )
    animal_usecase: AbstractAnimalUsecase = providers.Factory(
        AnimalUsecase,
        animal_repository=repositories.animal_repository,
        like_repository=repositories.like_repository,
        messaging=infrastructures.messaging,
        cache=infrastructures.cache,
        search=infrastructures.search,
    )
    like_usecase: AbstractLikeUsecase = providers.Factory(
        LikeUsecase,
        like_repository=repositories.like_repository,
    )
    violation_type_usecase: AbstractViolationTypeUsecase = providers.Factory(
        ViolationTypeUsecase, violation_type_repository=repositories.violation_type_repository
    )
    violation_usecase: AbstractViolationUsecase = providers.Factory(
        ViolationUsecase,
        violation_repository=repositories.violation_repository,
        animal_repository=repositories.animal_repository,
    )
    access_log_usecase: AbstractAccessLogUsecase = providers.Factory(
        AccessLogUsecase,
        access_log_repository=repositories.access_log_repository,
    )


class Jobs(containers.DeclarativeContainer):
    config = providers.Configuration()
    usecases = providers.DependenciesContainer()
    infrastructures = providers.DependenciesContainer()

    initialization_job: InitializationJob = providers.Factory(
        InitializationJob,
        table_usecase=usecases.table_usecase,
        animal_category_usecase=usecases.animal_category_usecase,
        animal_subcategory_usecase=usecases.animal_subcategory_usecase,
        user_usecase=usecases.user_usecase,
        animal_usecase=usecases.animal_usecase,
        violation_type_usecase=usecases.violation_type_usecase,
        violation_usecase=usecases.violation_usecase,
        like_usecase=usecases.like_usecase,
        access_log_usecase=usecases.access_log_usecase,
        messaging=infrastructures.messaging,
        database=infrastructures.database,
    )
    animal_search_job: AnimalToSearchJob = providers.Factory(
        AnimalToSearchJob,
        animal_usecase=usecases.animal_usecase,
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
        infrastructures=infrastructures,
    )
    jobs = providers.Container(
        Jobs,
        usecases=usecases,
        infrastructures=infrastructures,
    )
