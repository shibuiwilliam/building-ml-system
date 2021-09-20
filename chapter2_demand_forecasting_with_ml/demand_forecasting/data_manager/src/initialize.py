from logging import getLogger

from sqlalchemy import Column, Index
from sqlalchemy.engine import Engine
from src.configurations import Configurations
from src.container.container import container
from src.middleware.database import Base, get_context_db
from src.repository.item_arrival_repository import ItemArrivalModel
from src.repository.item_master_repository import ItemMasterModel
from src.repository.item_price_repository import ItemPriceModel
from src.repository.item_sale_prediction_repository import ItemSalePredictionModel
from src.repository.item_sale_repository import ItemSaleModel
from src.repository.item_stock_repository import ItemStockModel
from src.repository.region_master_repository import RegionMasterModel
from src.repository.store_master_repository import StoreMasterModel

logger = getLogger(name=__name__)


def create_tables(
    engine: Engine,
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
    create_index(
        table=ItemSaleModel,
        column=ItemSaleModel.sold_at,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=ItemSalePredictionModel,
        column=ItemSalePredictionModel.item_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=ItemSalePredictionModel,
        column=ItemSalePredictionModel.store_id,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )
    create_index(
        table=ItemSalePredictionModel,
        column=ItemSalePredictionModel.target_date,
        engine=engine,
        checkfirst=checkfirst,
        unique=False,
    )


def initialize_tables(
    engine: Engine,
    checkfirst: bool = True,
):
    create_tables(
        engine=engine,
        checkfirst=checkfirst,
    )
    create_indices(
        engine=engine,
        checkfirst=checkfirst,
    )


def initialize_data():
    with get_context_db() as db:
        container.store_service.initialize_region_master(
            db=db,
            file_path=Configurations.region_file_path,
        )
        container.store_service.initialize_store_master(
            db=db,
            file_path=Configurations.store_file_path,
        )
        container.item_service.initialize_item_master(
            db=db,
            file_path=Configurations.item_file_path,
        )
        container.item_service.initialize_item_price(
            db=db,
            file_path=Configurations.item_price_path,
        )
        container.item_service.initialize_item_sale(
            db=db,
            file_path=Configurations.item_sale_records_2017_2019_path,
        )
