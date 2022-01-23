from src.configurations import Configurations
from src.middleware.logger import configure_logger
from src.registry.container import container

logger = configure_logger(__name__)


def main():
    logger.info("START...")
    container.register_violation_job.run(queue_name=Configurations.violation_queue)


if __name__ == "__main__":
    main()
