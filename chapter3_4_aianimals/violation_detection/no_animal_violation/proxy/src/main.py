from dependency_injector.wiring import Provide, inject
from src.configurations import Configurations
from src.job.violation_detection_job import ViolationDetectionJob
from src.registry.container import Container
from time import sleep


@inject
def main(violation_detection_job: ViolationDetectionJob = Provide[Container.jobs.violation_detection_job]):
    if Configurations.off:
        while True:
            print("off...")
            sleep(10)

    violation_detection_job.run(
        consuming_queue=Configurations.consuming_queue,
        registration_queue=Configurations.registration_queue,
    )


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    main()
