import csv
from typing import List

from sqlalchemy import Column, Index
from sqlalchemy.engine import Engine
from src.middleware.logger import configure_logger
from src.repository.db import Base
from src.repository.item_arrival_repository import ItemArrivalModel
from src.repository.item_master_repository import ItemMasterModel
from src.repository.item_price_repository import ItemPriceModel
from src.repository.item_sale_repository import ItemSaleModel
from src.repository.item_stock_repository import ItemStockModel
from src.repository.region_master_repository import RegionMasterModel
from src.repository.store_master_repository import StoreMasterModel

logger = configure_logger(name=__name__)


def read_csv_data(
    file_path: str,
) -> List:
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]
    logger.debug(f"read data from {file_path}: {len(data)}")
    return data


def create_tables(
    engine,
    checkfirst: bool = True,
):
    logger.info("create tables")
    Base.metadata.create_all(
        engine,
        checkfirst=checkfirst,
    )
    logger.info("done create tables")


def create_index(
    table: Base,
    column: Column,
    engine: Engine,
    checkfirst: bool = True,
    unique: bool = False,
) -> Index:
    index_name = f"{table.__tablename__}_{column.name}_index"
    index = Index(
        index_name,
        column,
        unique=unique,
    )
    index.create(
        bind=engine,
        checkfirst=checkfirst,
    )
    logger.info(f"created index: {index_name}")
    return index


def create_indices(
    engine: Engine,
    checkfirst: bool = True,
):
    logger.info("create indices")

    create_index(
        table=RegionMasterModel,
        column=RegionMasterModel.name,
        engine=engine,
        checkfirst=checkfirst,
        unique=True,
    )
    create_index(
        table=StoreMasterModel,
        column=StoreMasterModel.name,
        engine=engine,
        checkfirst=checkfirst,
        unique=True,
    )
    create_index(
        table=StoreMasterModel,
        column=StoreMasterModel.region_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=ItemMasterModel,
        column=ItemMasterModel.name,
        engine=engine,
        checkfirst=checkfirst,
        unique=True,
    )
    create_index(
        table=ItemPriceModel,
        column=ItemPriceModel.item_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=ItemStockModel,
        column=ItemStockModel.item_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=ItemStockModel,
        column=ItemStockModel.store_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=ItemArrivalModel,
        column=ItemArrivalModel.item_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=ItemArrivalModel,
        column=ItemArrivalModel.store_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=ItemSaleModel,
        column=ItemSaleModel.item_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=ItemSaleModel,
        column=ItemSaleModel.store_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=ItemSaleModel,
        column=ItemSaleModel.item_price_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
