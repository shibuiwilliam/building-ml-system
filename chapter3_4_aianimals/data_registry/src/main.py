from src.configurations import Configurations
from src.middleware.logger import configure_logger
from src.registry.container import container

logger = configure_logger(__name__)


def main():
    logger.info("START...")
    container.table_controller.create_table()
    container.table_controller.create_index()
    container.animal_category_controller.register(
        session=container.database.get_session().__next__(),
        file_path=Configurations.animal_category_file,
    )
    container.animal_subcategory_controller.register(
        session=container.database.get_session().__next__(),
        file_path=Configurations.animal_subcategory_file,
    )
    container.user_controller.register(
        session=container.database.get_session().__next__(),
        file_path=Configurations.user_file,
    )
    container.animal_controller.register(
        session=container.database.get_session().__next__(),
        file_path=Configurations.animal_file,
    )
    logger.info("DONE...")


if __name__ == "__main__":
    main()
