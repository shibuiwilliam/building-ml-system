import logging.config

from database import DBClient
from dependency_injector.providers import Configuration, Container, DependenciesContainer, Factory, Resource, Singleton
from dependency_injector.containers import DeclarativeContainer
from model import AnimalRepository, ViolationRepository, ViolationTypeRepository
from view import ViolationListView
from view_model import AnimalViewModel, ViolationTypeViewModel, ViolationViewModel


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


class ViewModels(DeclarativeContainer):
    config = Configuration()
    models = DependenciesContainer()

    animal_view_model = Factory(
        AnimalViewModel,
        animal_repository=models.animal_repository,
    )
    violation_type_view_model = Factory(
        ViolationTypeViewModel,
        violation_type_repository=models.violation_type_repository,
    )
    violation_view_model = Factory(
        ViolationViewModel,
        violation_repository=models.violation_repository,
    )


class View(DeclarativeContainer):
    config = Configuration()
    view_models = DependenciesContainer()

    violation_list_view = Factory(
        ViolationListView,
        animal_view_model=view_models.animal_view_model,
        violation_type_view_model=view_models.violation_type_view_model,
        violation_view_model=view_models.violation_view_model,
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
    view_models = Container(
        ViewModels,
        config=config,
        models=models,
    )
    views = Container(
        View,
        config=config,
        view_models=view_models,
    )
