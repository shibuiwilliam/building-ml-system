import logging.config

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Container, DependenciesContainer, Factory, Resource, Singleton
from src.configurations import Configurations
from src.infrastructure.cache import AbstractCache, RedisCache
from src.infrastructure.database import AbstractDBClient, PostgresDBClient
from src.job.similar_word_registration_job import AbstractSimilarWordRegistrationJob, SimilarWordRegistrationJob
from src.repository.access_log_repository import AbstractAccessLogRepository, AccessLogRepository
from src.service.similar_word_predictor import AbstractSimilarWordPredictor, SimilarWordPredictor
from src.usecase.similar_word_usecase import AbstractSimilarWordUsecase, SimilarWordUsecase


class Core(DeclarativeContainer):
    config = Configuration()
    logging = Resource(
        logging.config.fileConfig,
        fname=Configurations.logging_file,
    )


class Infrastructures(DeclarativeContainer):
    config = Configuration()

    db_client: AbstractDBClient = Singleton(PostgresDBClient)
    cache_client: AbstractCache = Singleton(RedisCache)


class Services(DeclarativeContainer):
    config = Configuration()

    similar_word_predictor: AbstractSimilarWordPredictor = Singleton(
        SimilarWordPredictor,
        model_path=Configurations.model_path,
    )


class Models(DeclarativeContainer):
    config = Configuration()
    infrastructures = DependenciesContainer()

    access_log_repository: AbstractAccessLogRepository = Factory(
        AccessLogRepository,
        db_client=infrastructures.db_client,
    )


class Usecases(DeclarativeContainer):
    config = Configuration()
    infrastructures = DependenciesContainer()
    models = DependenciesContainer()
    services = DependenciesContainer()

    similar_word_usecase: AbstractSimilarWordUsecase = Factory(
        SimilarWordUsecase,
        access_log_repository=models.access_log_repository,
        cache_client=infrastructures.cache_client,
        similar_word_predictor=services.similar_word_predictor,
    )


class Jobs(DeclarativeContainer):
    config = Configuration()
    usecases = DependenciesContainer()

    similar_word_job: AbstractSimilarWordRegistrationJob = Factory(
        SimilarWordRegistrationJob,
        similar_word_usecase=usecases.similar_word_usecase,
    )


class Application(DeclarativeContainer):
    config = Configuration()

    core = Container(
        Core,
        config=config,
    )
    infrastructures = Container(
        Infrastructures,
        config=config,
    )
    services = Container(
        Services,
        config=config,
    )
    models = Container(
        Models,
        config=config,
        infrastructures=infrastructures,
    )
    usecases = Container(
        Usecases,
        config=config,
        infrastructures=infrastructures,
        models=models,
        services=services,
    )
    jobs = Container(
        Jobs,
        config=config,
        usecases=usecases,
    )
