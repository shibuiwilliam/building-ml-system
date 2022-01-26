from src.configurations import Configurations
from src.middleware.logger import configure_logger
from src.registry.container import container

logger = configure_logger(__name__)


def main():
    logger.info("START...")
    container.violation_detection_job.run(
        consuming_queue=Configurations.consuming_queue,
        registration_queue=Configurations.registration_queue,
    )


if __name__ == "__main__":
    main()
