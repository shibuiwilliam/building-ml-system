from time import sleep

from src.middleware.database import DBClient
from src.middleware.logger import configure_logger
from src.service.item_service import ItemService
from src.service.store_service import StoreService
from src.service.table_service import TableService

logger = configure_logger(__name__)


def main():
    sleep(10)
    logger.info("start jobs")
    db_client = DBClient()
    table_service = TableService(db_client=db_client)
    store_service = StoreService(db_client=db_client)
    item_service = ItemService(db_client=db_client)
    table_service.register()
    store_service.register()
    item_service.register()

    while True:
        logger.info("done...")
        sleep(120)


if __name__ == "__main__":
    main()
