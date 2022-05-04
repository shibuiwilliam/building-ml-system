from dependency_injector.wiring import Provide, inject
from src.registry.container import Application
from src.job.similar_word_registration_job import AbstractSimilarWordRegistrationJob


@inject
def main(similar_word_job: AbstractSimilarWordRegistrationJob = Provide[Application.jobs.similar_word_job]):
    similar_word_job.run()


if __name__ == "__main__":
    application = Application()
    application.core.init_resources()
    application.wire(modules=[__name__])

    main()
