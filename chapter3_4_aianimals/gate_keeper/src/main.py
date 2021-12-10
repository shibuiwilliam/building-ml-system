from src.middleware.logger import configure_logger
from src.registry.container import container

logger = configure_logger(__name__)


def main():
    logger.info("START...")
    container.animal_controller.run()


if __name__ == "__main__":
    main()
