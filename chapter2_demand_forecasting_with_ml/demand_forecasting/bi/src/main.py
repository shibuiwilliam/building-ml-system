from time import sleep

from configurations import Configurations
from db_client import DBClient
from logger import configure_logger
from view import build
from view_model import ItemSalesViewModel, ItemViewModel, RegionViewModel, StoreViewModel

logger = configure_logger(__name__)


def main():
    logger.info("now loading...")
    sleep(Configurations.wait_second)
    logger.info("start fun time")
    db_client = DBClient()
    region_view_model = RegionViewModel(db_client=db_client)
    store_view_model = StoreViewModel(db_client=db_client)
    item_view_model = ItemViewModel(db_client=db_client)
    item_sales_view_model = ItemSalesViewModel(db_client=db_client)
    build(
        region_view_model=region_view_model,
        store_view_model=store_view_model,
        item_view_model=item_view_model,
        item_sales_view_model=item_sales_view_model,
    )


if __name__ == "__main__":
    main()
