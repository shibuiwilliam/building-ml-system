from abc import ABCMeta, abstractmethod
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Extra
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import Integer
from src.middleware.logger import configure_logger
from src.repository.db import Base
from src.repository.item_master_repository import ItemMasterModel
from src.repository.item_price_repository import ItemPriceModel
from src.repository.store_master_repository import StoreMasterModel

logger = configure_logger(name=__name__)


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


class AbstractItemSaleRepository(metaclass=ABCMeta):
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
    ) -> List[ItemSale]:
        raise NotImplementedError

    @abstractmethod
    def record(
        self,
        db: Session,
        item_sale: ItemSaleCreate,
        commit: bool = True,
    ) -> Optional[ItemSale]:
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
    ) -> List[ItemSale]:
        filters = []
        if id is not None:
            filters.append(ItemSaleModel.id == id)
        if item_name is not None:
            filters.append(ItemMasterModel.name == item_id)
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
        records = (
            db.query(
                ItemSaleModel,
                ItemMasterModel,
                StoreMasterModel,
                ItemPriceModel,
            )
            .join(
                ItemMasterModel,
                ItemMasterModel.id == ItemSale.item_id,
                isout=True,
            )
            .join(
                StoreMasterModel,
                StoreMasterModel.id == ItemSale.store_id,
                isout=True,
            )
            .join(
                ItemPriceModel,
                ItemPriceModel.id == ItemSale.item_price_id,
                isout=True,
            )
            .filter(and_(*filters))
            .order_by(
                StoreMasterModel.name,
                ItemMasterModel.name,
                ItemSale.sold_at,
            )
            .all()
        )
        return [
            ItemSale(
                id=r.ItemSaleModel.id,
                item_id=r.ItemSaleModel.item_id,
                store_id=r.ItemSaleModel.store_id,
                quantity=r.ItemSaleModel.quantity,
                total_sales=r.ItemSale.total_sales,
                sold_at=r.ItemSaleModel.sold_at,
                item_name=r.ItemMasterModel.name,
                store_name=r.StoreMasterModel.name,
                price=r.ItemPriceModel.price,
                created_at=r.ItemSaleModel.created_at,
                updated_at=r.ItemSaleModel.updated_at,
            )
            for r in records
        ]

    def record(
        self,
        db: Session,
        item_sale: ItemSaleCreate,
        commit: bool = True,
    ) -> Optional[ItemSale]:
        data = ItemSaleModel(
            id=item_sale.id,
            item_id=item_sale.item_id,
            store_id=item_sale.store_id,
            item_price_id=item_sale.item_price_id,
            quantity=item_sale.quantity,
            total_sales=item_sale.total_sales,
            sold_at=item_sale.sold_at,
        )
        db.add(data)
        if commit:
            db.commit()
            db.refresh(data)
            records = self.retrieve(db=db, id=data.id)
            return ItemSale(
                id=records[0].id,
                item_id=records[0].item_id,
                store_id=records[0].store_id,
                item_price_id=records[0].item_price_id,
                quantity=records[0].quantity,
                total_sales=records[0].total_sales,
                sold_at=records[0].sold_at,
                item_name=records[0].item_name,
                store_name=records[0].store_name,
                price=records[0].price,
                created_at=records[0].created_at,
                updated_at=records[0].updated_at,
            )
        return None
