from dependency_injector.wiring import Provide, inject
from src.configurations import Configurations
from src.job.register_violation_job import RegisterViolationJob
from src.registry.container import Container


@inject
def main(register_violation_job: RegisterViolationJob = Provide[Container.jobs.register_violation_job]):
    register_violation_job.run(queue_name=Configurations.violation_queue)


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    main()
