from abc import ABC, abstractmethod
from datetime import date, datetime
from logging import getLogger
from typing import List, Optional

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
    def __init__(
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
    def retrieve_item_master(
        self,
        db: Session,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
    ) -> List[ItemMaster]:
        raise NotImplementedError

    @abstractmethod
    def retrieve_item_price(
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
    def retrieve_item_sale(
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
    def retrieve_item_sale_prediction(
        self,
        db: Session,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        store_name: Optional[str] = None,
        store_id: Optional[str] = None,
        target_date: Optional[date] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ItemSalePrediction]:
        raise NotImplementedError

    @abstractmethod
    def register_item_master(
        self,
        db: Session,
        name: str,
        id: str = get_uuid(),
    ) -> Optional[ItemMaster]:
        raise NotImplementedError

    @abstractmethod
    def register_item_price(
        self,
        db: Session,
        item_id: str,
        price: int,
        applied_from: date,
        applied_to: Optional[date] = None,
        id: str = get_uuid(),
    ) -> Optional[ItemPrice]:
        raise NotImplementedError

    @abstractmethod
    def register_item_sale(
        self,
        db: Session,
        item_id: str,
        store_id: str,
        item_price_id: str,
        quantity: int,
        sold_at: date,
        total_sales: Optional[int] = None,
        day_of_week: Optional[str] = None,
        id: str = get_uuid(),
    ) -> Optional[ItemSale]:
        raise NotImplementedError

    @abstractmethod
    def bulk_register_item_sale(
        self,
        db: Session,
        item_sales: List[ItemSaleCreate],
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def register_item_sale_prediction(
        self,
        db: Session,
        item_id: str,
        store_id: str,
        target_date: date,
        prediction: float,
        id: str = get_uuid(),
    ) -> Optional[ItemSalePrediction]:
        raise NotImplementedError

    @abstractmethod
    def bulk_register_item_sale_prediction(
        self,
        db: Session,
        item_sale_predictions: List[ItemSalePredictionCreate],
    ) -> int:
        raise NotImplementedError

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


class ItemService(AbstractItemService):
    def __init__(
        self,
        item_arrival_repository: AbstractItemArrivalRepository,
        item_master_repository: AbstractItemMasterRepository,
        item_price_repository: AbstractItemPriceRepository,
        item_sale_prediction_repository: AbstractItemSalePredictionRepository,
        item_sale_repository: AbstractItemSaleRepository,
        item_stock_repository: AbstractItemStockRepository,
    ):
        super().__init__(
            item_arrival_repository=item_arrival_repository,
            item_master_repository=item_master_repository,
            item_price_repository=item_price_repository,
            item_sale_prediction_repository=item_sale_prediction_repository,
            item_sale_repository=item_sale_repository,
            item_stock_repository=item_stock_repository,
        )
        self.weekdays = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

    def retrieve_item_master(
        self,
        db: Session,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
    ) -> List[ItemMaster]:
        result = self.item_master_repository.retrieve(
            db=db,
            id=id,
            name=item_name,
        )
        return result

    def retrieve_item_price(
        self,
        db: Session,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        applied_from: Optional[date] = None,
        applied_to: Optional[date] = None,
    ) -> List[ItemPrice]:
        result = self.item_price_repository.retrieve(
            db=db,
            id=id,
            item_name=item_name,
            item_id=item_id,
            applied_from=applied_from,
            applied_to=applied_to,
        )
        return result

    def retrieve_item_sale(
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
        result = self.item_sale_repository.retrieve(
            db=db,
            id=id,
            item_name=item_name,
            item_id=item_id,
            store_name=store_name,
            store_id=store_id,
            item_price_id=item_price_id,
            quantity=quantity,
            sold_at=sold_at,
            day_of_week=day_of_week,
            limit=limit,
            offset=offset,
        )
        return result

    def retrieve_item_sale_prediction(
        self,
        db: Session,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        store_name: Optional[str] = None,
        store_id: Optional[str] = None,
        target_date: Optional[date] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ItemSalePrediction]:
        result = self.item_sale_prediction_repository.retrieve(
            db=db,
            id=id,
            item_name=item_name,
            item_id=item_id,
            store_name=store_name,
            store_id=store_id,
            target_date=target_date,
            limit=limit,
            offset=offset,
        )
        return result

    def register_item_master(
        self,
        db: Session,
        name: str,
        id: str = get_uuid(),
    ) -> Optional[ItemMaster]:
        result = self.item_master_repository.register(
            db=db,
            item_master=ItemMasterCreate(
                id=id,
                name=name,
            ),
            commit=True,
        )
        return result

    @abstractmethod
    def register_item_price(
        self,
        db: Session,
        item_id: str,
        price: int,
        applied_from: date,
        applied_to: Optional[date] = None,
        id: str = get_uuid(),
    ) -> Optional[ItemPrice]:
        result = self.item_price_repository.register(
            db=db,
            item_price=ItemPriceCreate(
                id=id,
                item_id=item_id,
                price=price,
                applied_from=applied_from,
                applied_to=applied_to,
            ),
            commit=True,
        )
        return result

    @abstractmethod
    def register_item_sale(
        self,
        db: Session,
        item_id: str,
        store_id: str,
        item_price_id: str,
        quantity: int,
        sold_at: date,
        total_sales: Optional[int] = None,
        day_of_week: Optional[str] = None,
        id: str = get_uuid(),
    ) -> Optional[ItemSale]:
        if day_of_week is None or day_of_week not in self.weekdays:
            dt = sold_at.weekday()
            day_of_week = self.weekdays[dt]
        if total_sales is None:
            prices = self.item_price_repository.retrieve(db=db, id=item_price_id)
            total_sales = quantity * prices[0].price
        result = self.item_sale_repository.register(
            db=db,
            item_sale=ItemSaleCreate(
                id=id,
                item_id=item_id,
                store_id=store_id,
                item_price_id=item_price_id,
                quantity=quantity,
                total_sales=total_sales,
                sold_at=sold_at,
                day_of_week=day_of_week,
            ),
            commit=True,
        )
        return result

    def bulk_register_item_sale(
        self,
        db: Session,
        item_sales: List[ItemSaleCreate],
    ) -> int:
        results = 0
        _item_sales = []
        for i, data in enumerate(item_sales):
            _item_sales.append(data)
            if i % 5000 == 0:
                result = self.item_sale_repository.bulk_register(
                    db=db,
                    item_sales=_item_sales,
                    commit=True,
                )
                results += result
                _item_sales = []
                logger.info(f"registered: {results}...")
        if len(_item_sales) > 0:
            result = self.item_sale_repository.bulk_register(
                db=db,
                item_sales=_item_sales,
                commit=True,
            )
            results += result
        logger.info(f"total registered: {results}")
        return results

    def register_item_sale_prediction(
        self,
        db: Session,
        item_id: str,
        store_id: str,
        target_date: date,
        prediction: float,
        id: str = get_uuid(),
    ) -> Optional[ItemSalePrediction]:
        result = self.item_sale_prediction_repository.register(
            db=db,
            item_sale_prediction=ItemSalePredictionCreate(
                id=id,
                item_id=item_id,
                store_id=store_id,
                target_date=target_date,
                prediction=prediction,
            ),
            commit=True,
        )
        return result

    @abstractmethod
    def bulk_register_item_sale_prediction(
        self,
        db: Session,
        item_sale_predictions: List[ItemSalePredictionCreate],
        commit: bool = True,
    ) -> int:
        results = 0
        _item_sale_predictions = []
        for i, data in enumerate(item_sale_predictions):
            _item_sale_predictions.append(data)
            if i % 5000 == 0:
                result = self.item_sale_prediction_repository.bulk_register(
                    db=db,
                    item_sale_predictions=_item_sale_predictions,
                    commit=True,
                )
                results += result
                _item_sale_predictions = []
                logger.info(f"registered: {results}...")
        if len(_item_sale_predictions) > 0:
            result = self.item_sale_prediction_repository.bulk_register(
                db=db,
                item_sale_predictions=_item_sale_predictions,
                commit=True,
            )
            results += result
        logger.info(f"total registered: {results}")
        return results

    def initialize_item_master(
        self,
        db: Session,
        file_path: str,
    ) -> int:
        dataset = read_csv_data(file_path=file_path)
        results = []
        for data in dataset:
            result = self.register_item_master(
                db=db,
                name=data["name"],
                id=data["id"],
            )
            results.append(result)
        logger.info(f"{file_path} registered item master: {results}")
        return len(results)

    def initialize_item_price(
        self,
        db: Session,
        file_path: str,
    ) -> int:
        dataset = read_csv_data(file_path=file_path)
        results = []
        for data in dataset:
            result = self.register_item_price(
                db=db,
                id=data["id"],
                item_id=data["id"],
                price=int(data["price"]),
                applied_from=datetime.strptime(data["applied_from"], "%Y-%m-%d"),
                applied_to=datetime.strptime(data["applied_to"], "%Y-%m-%d")
                if data["applied_to"] is not None
                else None,
            )
            results.append(result)
        logger.info(f"{file_path} registered item price: {results}")
        return len(results)

    def initialize_item_sale(
        self,
        db: Session,
        file_path: str,
    ) -> int:
        dataset = read_csv_data(file_path=file_path)
        item_sales = [
            ItemSaleCreate(
                id=get_uuid(),
                item_id=data["item_id"],
                store_id=data["store_id"],
                item_price_id=data["item_price_id"],
                quantity=int(data["quantity"]),
                total_sales=int(data["total_sales"]),
                sold_at=datetime.strptime(data["date"], "%Y-%m-%d"),
                day_of_week=data["day_of_week"],
            )
            for data in dataset
        ]
        results = self.bulk_register_item_sale(db=db, item_sales=item_sales)
        logger.info(f"{file_path} total registered item sales: {results}")
        return results
