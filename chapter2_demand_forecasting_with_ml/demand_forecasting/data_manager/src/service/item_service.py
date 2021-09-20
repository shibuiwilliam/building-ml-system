from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional
from datetime import date

from sqlalchemy.orm import Session
from src.middleware.file_reader import read_csv_data
from src.middleware.strings import get_uuid
from src.repository.item_arrival_repository import AbstractItemArrivalRepository, ItemArrival, ItemArrivalCreate
from src.repository.item_master_repository import AbstractItemMasterRepository, ItemMaster, ItemMasterCreate
from src.repository.item_price_repository import AbstractItemPriceRepository, ItemPrice, ItemPriceCreate
from src.repository.item_sale_prediction_repository import (
    AbstractItemSalePredictionRepository,
    ItemSalePrediction,
    ItemSalePredictionCreate,
)
from src.repository.item_sale_repository import AbstractItemSaleRepository, ItemSale, ItemSaleCreate
from src.repository.item_stock_repository import AbstractItemStockRepository, ItemStock, ItemStockCreate


logger = getLogger(name=__name__)


class AbstractItemService(ABC):
    def init(
        self,
        item_arrival_repository: AbstractItemArrivalRepository,
        item_master_repository: AbstractItemMasterRepository,
        item_price_repository: AbstractItemPriceRepository,
        item_sale_prediction_repository: AbstractItemSalePredictionRepository,
        item_sale_repository: AbstractItemSaleRepository,
        item_stock_repository: AbstractItemStockRepository,
    ):
        self.item_arrival_repository = item_arrival_repository
        self.item_master_repository = item_master_repository
        self.item_price_repository = item_price_repository
        self.item_sale_prediction_repository = item_sale_prediction_repository
        self.item_sale_repository = item_sale_repository
        self.item_stock_repository = item_stock_repository

    @abstractmethod
    def initialize_item_master(
        self,
        db: Session,
        file_path: str,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def initialize_item_price(
        self,
        db: Session,
        file_path: str,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def initialize_item_sale(
        self,
        db: Session,
        file_path: str,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def register_item_master(
        self,
        db: Session,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> List[ItemMaster]:
        raise NotImplementedError

    @abstractmethod
    def register_item_price(
        self,
        db: Session,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        applied_from: Optional[date] = None,
        applied_to: Optional[date] = None,
    ) -> List[ItemPrice]:
        raise NotImplementedError

    @abstractmethod
    def register_item_sale(
        self,
        db: Session,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        store_name: Optional[str] = None,
        store_id: Optional[str] = None,
        item_price_id: Optional[str] = None,
        quantity: Optional[int] = None,
        sold_at: Optional[date] = None,
        day_of_week: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ItemSale]:
        raise NotImplementedError

    @abstractmethod
    def bulk_register_item_sale(
        self,
        db: Session,
        item_sales: List[ItemSaleCreate],
        commit: bool = True,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def register_item_sale_prediction(
        self,
        db: Session,
        item_sale_prediction: ItemSalePredictionCreate,
        commit: bool = True,
    ) -> Optional[ItemSalePrediction]:
        raise NotImplementedError

    @abstractmethod
    def bulk_register_item_sale_prediction(
        self,
        db: Session,
        item_sale_predictions: List[ItemSalePredictionCreate],
        commit: bool = True,
    ) -> int:
        raise NotImplementedError
