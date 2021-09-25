from abc import ABC, abstractmethod
from datetime import date, datetime
from logging import getLogger
from typing import List, Optional

from pydantic import BaseModel, Extra
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import Integer
from src.middleware.database import Base
from src.repository.item_master_repository import ItemMasterModel
from src.repository.item_price_repository import ItemPriceModel
from src.repository.store_master_repository import StoreMasterModel

logger = getLogger(name=__name__)


class ItemSaleModel(Base):
    __tablename__ = "item_sales"

    id = Column(
        String(32),
        nullable=False,
        primary_key=True,
    )
    item_id = Column(
        String(32),
        ForeignKey("item_master.id"),
        nullable=False,
    )
    store_id = Column(
        String(32),
        ForeignKey("store_master.id"),
        nullable=False,
    )
    item_price_id = Column(
        String(32),
        ForeignKey("item_prices.id"),
        nullable=False,
    )
    quantity = Column(
        Integer,
        nullable=False,
    )
    total_sales = Column(
        Integer,
        nullable=False,
    )
    sold_at = Column(
        Date,
        nullable=False,
    )
    day_of_week = Column(
        String(3),
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )


class ItemSaleBase(BaseModel):
    id: str
    item_id: str
    store_id: str
    item_price_id: str
    quantity: int
    total_sales: int
    sold_at: date
    day_of_week: str


class ItemSaleCreate(ItemSaleBase):
    pass

    class Config:
        extra = Extra.forbid


class ItemSale(ItemSaleBase):
    item_name: str
    store_name: str
    price: int
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class AbstractItemSaleRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def retrieve(
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
    def register(
        self,
        db: Session,
        item_sale: ItemSaleCreate,
        commit: bool = True,
    ) -> Optional[ItemSale]:
        raise NotImplementedError

    @abstractmethod
    def bulk_register(
        self,
        db: Session,
        item_sales: List[ItemSaleCreate],
        commit: bool = True,
    ) -> int:
        raise NotImplementedError


class ItemSaleRepository(AbstractItemSaleRepository):
    def __init__(self):
        pass

    def retrieve(
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
        filters = []
        if id is not None:
            filters.append(ItemSaleModel.id == id)
        if item_name is not None:
            filters.append(ItemMasterModel.name == item_name)
        if item_id is not None:
            filters.append(ItemSaleModel.item_id == item_id)
        if store_name is not None:
            filters.append(StoreMasterModel.name == store_name)
        if store_id is not None:
            filters.append(ItemSaleModel.store_id == store_id)
        if item_price_id is not None:
            filters.append(ItemSaleModel.item_price_id == item_price_id)
        if quantity is not None:
            filters.append(ItemSaleModel.quantity == quantity)
        if sold_at is not None:
            filters.append(ItemSaleModel.sold_at == sold_at)
        if day_of_week is not None:
            filters.append(ItemSaleModel.day_of_week == day_of_week)
        records = (
            db.query(
                ItemSaleModel,
                ItemMasterModel,
                StoreMasterModel,
                ItemPriceModel,
            )
            .join(
                ItemMasterModel,
                ItemMasterModel.id == ItemSaleModel.item_id,
                isouter=True,
            )
            .join(
                StoreMasterModel,
                StoreMasterModel.id == ItemSaleModel.store_id,
                isouter=True,
            )
            .join(
                ItemPriceModel,
                ItemPriceModel.id == ItemSaleModel.item_price_id,
                isouter=True,
            )
            .filter(and_(*filters))
            .order_by(
                StoreMasterModel.name,
                ItemMasterModel.name,
                ItemSaleModel.sold_at,
            )
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [
            ItemSale(
                id=r.ItemSaleModel.id,
                item_id=r.ItemSaleModel.item_id,
                store_id=r.ItemSaleModel.store_id,
                item_price_id=r.ItemSaleModel.item_price_id,
                quantity=r.ItemSaleModel.quantity,
                total_sales=r.ItemSaleModel.total_sales,
                sold_at=r.ItemSaleModel.sold_at,
                day_of_week=r.ItemSaleModel.day_of_week,
                item_name=r.ItemMasterModel.name,
                store_name=r.StoreMasterModel.name,
                price=r.ItemPriceModel.price,
                created_at=r.ItemSaleModel.created_at,
                updated_at=r.ItemSaleModel.updated_at,
            )
            for r in records
        ]

    def register(
        self,
        db: Session,
        item_sale: ItemSaleCreate,
        commit: bool = True,
    ) -> Optional[ItemSale]:
        data = ItemSaleModel(**item_sale.dict())
        db.add(data)
        if commit:
            db.commit()
            db.refresh(data)
            records = self.retrieve(
                db=db,
                id=data.id,
            )
            return records[0]
        return None

    def bulk_register(
        self,
        db: Session,
        item_sales: List[ItemSaleCreate],
        commit: bool = True,
    ) -> int:
        data = [ItemSaleModel(**item_sale.dict()) for item_sale in item_sales]
        db.bulk_save_objects(data)
        if commit:
            db.commit()
            return len(data)
        return 0
