from time import sleep
from typing import Optional, Tuple

import click
from src.infrastructure.database import PostgreSQLClient
from src.middleware.logger import configure_logger
from src.service.item_service import ItemService
from src.service.store_service import StoreService
from src.service.table_service import TableService

logger = configure_logger(__name__)


@click.command()
@click.option(
    "--init_sql_file_path",
    type=str,
    required=False,
)
@click.option(
    "--region_store_file_paths",
    type=(str, str),
    required=False,
)
@click.option(
    "--item_file_paths",
    type=(str, str),
    required=False,
)
@click.option(
    "--item_sales_records_path",
    type=str,
    required=False,
)
def main(
    init_sql_file_path: Optional[str] = None,
    region_store_file_paths: Optional[Tuple[str, str]] = None,
    item_file_paths: Optional[Tuple[str, str]] = None,
    item_sales_records_path: Optional[str] = None,
):
    logger.info("start jobs")
    logger.info(
        f"""
options:
    init_sql_file_path: {init_sql_file_path}
    region_store_file_paths: {region_store_file_paths}
    item_file_paths: {item_file_paths}
    item_sales_records_path: {item_sales_records_path}
    """
    )
    db_client = PostgreSQLClient()

    table_service = TableService(db_client=db_client)
    store_service = StoreService(db_client=db_client)
    item_service = ItemService(db_client=db_client)

    if init_sql_file_path is not None:
        table_service.register(sql_file_path=init_sql_file_path)

    if region_store_file_paths is not None:
        store_service.register(
            region_file_path=region_store_file_paths[0],
            store_file_path=region_store_file_paths[1],
        )

    if item_file_paths is not None:
        item_service.register(
            item_file_path=item_file_paths[0],
            item_price_path=item_file_paths[1],
        )

    if item_sales_records_path is not None:
        item_service.register_records(item_sales_records_path=item_sales_records_path)

    while True:
        logger.info("done...")
        sleep(120)


if __name__ == "__main__":
    main()
