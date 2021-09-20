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
from src.repository.store_master_repository import StoreMasterModel

logger = getLogger(name=__name__)


class ItemStockModel(Base):
    __tablename__ = "item_stocks"

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
    stock = Column(
        Integer,
        nullable=False,
    )
    recorded_at = Column(
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


class ItemStockBase(BaseModel):
    id: str
    item_id: str
    store_id: str
    stock: int
    recorded_at: date


class ItemStockCreate(ItemStockBase):
    pass

    class Config:
        extra = Extra.forbid


class ItemStock(ItemStockBase):
    item_name: str
    store_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class AbstractItemStockRepository(ABC):
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
        recorded_at: Optional[date] = None,
    ) -> List[ItemStock]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        db: Session,
        item_stock: ItemStockCreate,
        commit: bool = True,
    ) -> Optional[ItemStock]:
        raise NotImplementedError


class ItemStockRepository(AbstractItemStockRepository):
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
        recorded_at: Optional[date] = None,
    ) -> List[ItemStock]:
        filters = []
        if id is not None:
            filters.append(ItemStockModel.id == id)
        if item_name is not None:
            filters.append(ItemMasterModel.name == item_id)
        if item_id is not None:
            filters.append(ItemStockModel.item_id == item_id)
        if store_name is not None:
            filters.append(StoreMasterModel.name == store_name)
        if store_id is not None:
            filters.append(ItemStockModel.store_id == store_id)
        if recorded_at is not None:
            filters.append(ItemStockModel.recorded_at == recorded_at)
        records = (
            db.query(ItemStockModel, ItemMasterModel, StoreMasterModel)
            .join(
                ItemMasterModel,
                ItemMasterModel.id == ItemStock.item_id,
                isouter=True,
            )
            .join(
                StoreMasterModel,
                StoreMasterModel.id == ItemStock.store_id,
                isouter=True,
            )
            .filter(and_(*filters))
            .order_by(
                StoreMasterModel.name,
                ItemMasterModel.name,
                ItemStockModel.recorded_at,
            )
            .all()
        )
        return [
            ItemStock(
                id=r.ItemStockModel.id,
                item_id=r.ItemStockModel.item_id,
                store_id=r.ItemStockModel.store_id,
                stock=r.ItemStockModel.stock,
                recorded_at=r.ItemStockModel.recorded_at,
                item_name=r.ItemMasterModel.name,
                store_name=r.StoreMasterModel.name,
                created_at=r.ItemStockModel.created_at,
                updated_at=r.ItemStockModel.updated_at,
            )
            for r in records
        ]

    def register(
        self,
        db: Session,
        item_stock: ItemStockCreate,
        commit: bool = True,
    ) -> Optional[ItemStock]:
        is_exists = self.retrieve(
            db=db,
            item_id=item_stock.item_id,
            recorded_at=item_stock.recorded_at,
        )
        if len(is_exists) > 0:
            return is_exists[0]
        data = ItemStockModel(**item_stock.dict())
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
