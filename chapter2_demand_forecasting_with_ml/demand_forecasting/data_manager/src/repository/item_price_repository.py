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

logger = getLogger(name=__name__)


class ItemPriceModel(Base):
    __tablename__ = "item_prices"

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
    price = Column(
        Integer,
        nullable=False,
    )
    applied_from = Column(
        Date,
        nullable=False,
    )
    applied_to = Column(
        Date,
        nullable=True,
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


class ItemPriceBase(BaseModel):
    id: str
    item_id: str
    price: int
    applied_from: date
    applied_to: Optional[date]


class ItemPriceCreate(ItemPriceBase):
    pass

    class Config:
        extra = Extra.forbid


class ItemPriceUpdate(BaseModel):
    id: str
    item_id: str
    price: int
    applied_from: date
    applied_to: date

    class Config:
        extra = Extra.forbid


class ItemPrice(ItemPriceBase):
    item_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class AbstractItemPriceRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def retrieve(
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
    def register(
        self,
        db: Session,
        item_price: ItemPriceCreate,
        commit: bool = True,
    ) -> Optional[ItemPrice]:
        raise NotImplementedError


class ItemPriceRepository(AbstractItemPriceRepository):
    def __init__(self):
        pass

    def retrieve(
        self,
        db: Session,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        applied_from: Optional[date] = None,
        applied_to: Optional[date] = None,
    ) -> List[ItemPrice]:
        filters = []
        if id is not None:
            filters.append(ItemPriceModel.id == id)
        if item_name is not None:
            filters.append(ItemMasterModel.name == item_id)
        if item_id is not None:
            filters.append(ItemPriceModel.item_id == item_id)
        if applied_from is not None:
            filters.append(ItemPriceModel.applied_from <= applied_from)
        if applied_to is not None:
            filters.append(ItemPriceModel.applied_to >= applied_to)
        records = (
            db.query(ItemPriceModel, ItemMasterModel)
            .join(
                ItemMasterModel,
                ItemMasterModel.id == ItemPriceModel.item_id,
                isouter=True,
            )
            .filter(and_(*filters))
            .order_by(
                ItemMasterModel.name,
                ItemPriceModel.applied_from,
            )
            .all()
        )
        return [
            ItemPrice(
                id=r.ItemPriceModel.id,
                item_name=r.ItemMasterModel.name,
                item_id=r.ItemPriceModel.item_id,
                price=r.ItemPriceModel.price,
                applied_from=r.ItemPriceModel.applied_from,
                applied_to=r.ItemPriceModel.applied_to,
                created_at=r.ItemPriceModel.created_at,
                updated_at=r.ItemPriceModel.updated_at,
            )
            for r in records
        ]

    def register(
        self,
        db: Session,
        item_price: ItemPriceCreate,
        commit: bool = True,
    ) -> Optional[ItemPrice]:
        is_exists = self.retrieve(
            db=db,
            item_id=item_price.item_id,
            applied_from=item_price.applied_from,
            applied_to=item_price.applied_to,
        )
        if len(is_exists) > 0:
            return is_exists[0]
        data = ItemPriceModel(**item_price.dict())
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
