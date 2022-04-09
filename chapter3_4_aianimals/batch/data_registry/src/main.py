from dependency_injector.wiring import Provide, inject
from src.configurations import Configurations
from src.job.animal_to_search_job import AnimalToSearchJob
from src.job.initialization_job import InitializationJob
from src.job.jobs import JOBS
from src.registry.container import Container


@inject
def main(
    initialization_job: InitializationJob = Provide[Container.jobs.initialization_job],
    animal_search_job: AnimalToSearchJob = Provide[Container.jobs.animal_search_job],
):
    if Configurations.job == JOBS.ANIMAL_TO_SEARCH_JOB.value.name:
        animal_search_job.run()
    elif Configurations.job == JOBS.INITIALIZATION_JOG.value.name:
        initialization_job.run()
    else:
        raise ValueError


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    main()
