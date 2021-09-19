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
from src.repository.store_master_repository import StoreMasterModel

logger = configure_logger(name=__name__)


class ItemArrivalModel(Base):
    __tablename__ = "item_arrivals"

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
    quantity = Column(
        Integer,
        nullable=False,
    )
    arrived_at = Column(
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


class ItemArrivalBase(BaseModel):
    id: str
    item_id: str
    store_id: str
    quantity: int
    arrived_at: date


class ItemArrivalCreate(ItemArrivalBase):
    pass

    class Config:
        extra = Extra.forbid


class ItemArrival(ItemArrivalBase):
    item_name: str
    store_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class AbstractItemArrivalRepository(metaclass=ABCMeta):
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
        arrived_at: Optional[date] = None,
    ) -> List[ItemArrival]:
        raise NotImplementedError

    @abstractmethod
    def record(
        self,
        db: Session,
        item_arrival: ItemArrivalCreate,
        commit: bool = True,
    ) -> Optional[ItemArrival]:
        raise NotImplementedError


class ItemArrivalRepository(AbstractItemArrivalRepository):
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
        arrived_at: Optional[date] = None,
    ) -> List[ItemArrival]:
        filters = []
        if id is not None:
            filters.append(ItemArrivalModel.id == id)
        if item_name is not None:
            filters.append(ItemMasterModel.name == item_id)
        if item_id is not None:
            filters.append(ItemArrivalModel.item_id == item_id)
        if store_name is not None:
            filters.append(StoreMasterModel.name == store_name)
        if store_id is not None:
            filters.append(ItemArrivalModel.store_id == store_id)
        if arrived_at is not None:
            filters.append(ItemArrivalModel.arrived_at == arrived_at)
        records = (
            db.query(ItemArrivalModel, ItemMasterModel, StoreMasterModel)
            .join(
                ItemMasterModel,
                ItemMasterModel.id == ItemArrival.item_id,
                isout=True,
            )
            .join(
                StoreMasterModel,
                StoreMasterModel.id == ItemArrival.store_id,
                isout=True,
            )
            .filter(and_(*filters))
            .order_by(
                StoreMasterModel.name,
                ItemMasterModel.name,
                ItemArrivalModel.arrived_at,
            )
            .all()
        )
        return [
            ItemArrival(
                id=r.ItemArrivalModel.id,
                item_id=r.ItemArrivalModel.item_id,
                store_id=r.ItemArrivalModel.store_id,
                quantity=r.ItemArrivalModel.quantity,
                arrived_at=r.ItemArrivalModel.arrived_at,
                item_name=r.ItemMasterModel.name,
                store_name=r.StoreMasterModel.name,
                created_at=r.ItemArrivalModel.created_at,
                updated_at=r.ItemArrivalModel.updated_at,
            )
            for r in records
        ]

    def record(
        self,
        db: Session,
        item_arrival: ItemArrivalCreate,
        commit: bool = True,
    ) -> Optional[ItemArrival]:
        is_exists = self.retrieve(
            db=db,
            item_id=item_arrival.item_id,
            arrived_at=item_arrival.arrived_at,
        )
        if len(is_exists) > 0:
            return is_exists[0]
        data = ItemArrivalModel(
            id=item_arrival.id,
            item_id=item_arrival.item_id,
            store_id=item_arrival.store_id,
            quantity=item_arrival.quantity,
            arrived_at=item_arrival.arrived_at,
        )
        db.add(data)
        if commit:
            db.commit()
            db.refresh(data)
            return ItemArrival(
                id=data.id,
                item_id=data.item_id,
                store_id=data.store_id,
                arrived_at=data.arrived_at,
                created_at=data.created_at,
                updated_at=data.updated_at,
            )
        return None
