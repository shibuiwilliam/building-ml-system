import logging.config

from database import DBClient
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Container, DependenciesContainer, Factory, Resource, Singleton
from model import AnimalRepository, ViolationRepository, ViolationTypeRepository
from service import AnimalService, ViolationService, ViolationTypeService
from view import SidePane, ViolationCheckView, ViolationListView


class Core(DeclarativeContainer):
    config = Configuration()
    logging = Resource(
        logging.config.fileConfig,
        fname="src/logging.ini",
    )


class Infrastructures(DeclarativeContainer):
    config = Configuration()

    db_client = Singleton(DBClient)


class Models(DeclarativeContainer):
    config = Configuration()
    infrastructures = DependenciesContainer()

    animal_repository = Factory(
        AnimalRepository,
        db_client=infrastructures.db_client,
    )
    violation_type_repository = Factory(
        ViolationTypeRepository,
        db_client=infrastructures.db_client,
    )
    violation_repository = Factory(
        ViolationRepository,
        db_client=infrastructures.db_client,
    )


class Services(DeclarativeContainer):
    config = Configuration()
    models = DependenciesContainer()

    animal_service = Factory(
        AnimalService,
        animal_repository=models.animal_repository,
        violation_repository=models.violation_repository,
    )
    violation_type_service = Factory(
        ViolationTypeService,
        violation_type_repository=models.violation_type_repository,
    )
    violation_service = Factory(
        ViolationService,
        animal_repository=models.animal_repository,
        violation_repository=models.violation_repository,
    )


class View(DeclarativeContainer):
    config = Configuration()
    services = DependenciesContainer()

    violation_list_view = Factory(
        ViolationListView,
        animal_service=services.animal_service,
        violation_type_service=services.violation_type_service,
        violation_service=services.violation_service,
    )
    violation_check_view = Factory(
        ViolationCheckView,
        animal_service=services.animal_service,
        violation_type_service=services.violation_type_service,
        violation_service=services.violation_service,
    )
    side_pane = Factory(
        SidePane,
        violation_list_view=violation_list_view,
        violation_check_view=violation_check_view,
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
    models = Container(
        Models,
        config=config,
        infrastructures=infrastructures,
    )
    services = Container(
        Services,
        config=config,
        models=models,
    )
    views = Container(
        View,
        config=config,
        services=services,
    )
