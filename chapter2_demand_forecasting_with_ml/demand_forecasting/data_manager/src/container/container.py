from logging import getLogger

from src.repository.item_arrival_repository import AbstractItemArrivalRepository, ItemArrivalRepository
from src.repository.item_master_repository import AbstractItemMasterRepository, ItemMasterRepository
from src.repository.item_price_repository import AbstractItemPriceRepository, ItemPriceRepository
from src.repository.item_sale_prediction_repository import (
    AbstractItemSalePredictionRepository,
    ItemSalePredictionRepository,
)
from src.repository.item_sale_repository import AbstractItemSaleRepository, ItemSaleRepository
from src.repository.item_stock_repository import AbstractItemStockRepository, ItemStockRepository
from src.repository.region_master_repository import AbstractRegionMasterRepository, RegionMasterRepository
from src.repository.store_master_repository import AbstractStoreMasterRepository, StoreMasterRepository
from src.service.item_service import AbstractItemService, ItemService
from src.service.store_service import AbstractStoreService, StoreService


class Container(object):
    def __init__(self):
        self.__item_arrival_repository: AbstractItemArrivalRepository = ItemArrivalRepository()
        self.__item_master_repository: AbstractItemMasterRepository = ItemMasterRepository()
        self.__item_price_repository: AbstractItemPriceRepository = ItemPriceRepository()
        self.__item_sale_prediction_repository: AbstractItemSalePredictionRepository = ItemSalePredictionRepository()
        self.__item_sale_repository: AbstractItemSaleRepository = ItemSaleRepository()
        self.__item_stock_repository: AbstractItemStockRepository = ItemStockRepository()
        self.__store_master_repository: AbstractStoreMasterRepository = StoreMasterRepository()
        self.__region_master_repository: AbstractRegionMasterRepository = RegionMasterRepository()

        self.store_service: AbstractStoreService = StoreService(
            region_master_repository=self.__region_master_repository,
            store_master_repository=self.__store_master_repository,
        )
        self.item_service: AbstractItemService = ItemService(
            item_arrival_repository=self.__item_arrival_repository,
            item_master_repository=self.__item_master_repository,
            item_price_repository=self.__item_price_repository,
            item_sale_prediction_repository=self.__item_sale_prediction_repository,
            item_sale_repository=self.__item_sale_repository,
            item_stock_repository=self.__item_stock_repository,
        )


container = Container()
