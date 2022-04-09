from dependency_injector.wiring import Provide, inject
from src.configurations import Configurations
from src.registry.container import Container


@inject
def main(violation_detection_job: Provide[Container.jobs.violation_detection_job]):
    violation_detection_job.run(
        consuming_queue=Configurations.consuming_queue,
        registration_queue=Configurations.registration_queue,
    )


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    main()
