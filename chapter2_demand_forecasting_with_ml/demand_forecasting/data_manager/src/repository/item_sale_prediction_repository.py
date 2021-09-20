from abc import ABC, abstractmethod
from datetime import date, datetime
from logging import getLogger
from typing import List, Optional

from pydantic import BaseModel, Extra
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, String, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
from src.middleware.database import Base
from src.repository.item_master_repository import ItemMasterModel
from src.repository.store_master_repository import StoreMasterModel

logger = getLogger(name=__name__)


class ItemSalePredictionModel(Base):
    __tablename__ = "item_sale_predictions"

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
    target_date = Column(
        Date,
        nullable=False,
    )
    prediction = Column(
        Float,
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


class ItemSalePredictionBase(BaseModel):
    id: str
    item_id: str
    store_id: str
    target_date: date
    prediction: float


class ItemSalePredictionCreate(ItemSalePredictionBase):
    pass

    class Config:
        extra = Extra.forbid


class ItemSalePrediction(ItemSalePredictionBase):
    item_name: str
    store_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class AbstractItemSalePredictionRepository(ABC):
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
        target_date: Optional[date] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ItemSalePrediction]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        db: Session,
        item_sale_prediction: ItemSalePredictionCreate,
        commit: bool = True,
    ) -> Optional[ItemSalePrediction]:
        raise NotImplementedError

    @abstractmethod
    def bulk_register(
        self,
        db: Session,
        item_sale_predictions: List[ItemSalePredictionCreate],
        commit: bool = True,
    ) -> int:
        raise NotImplementedError


class ItemSalePredictionRepository(AbstractItemSalePredictionRepository):
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
        target_date: Optional[date] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ItemSalePrediction]:
        filters = []
        if id is not None:
            filters.append(ItemSalePredictionModel.id == id)
        if item_name is not None:
            filters.append(ItemMasterModel.name == item_id)
        if item_id is not None:
            filters.append(ItemSalePredictionModel.item_id == item_id)
        if store_name is not None:
            filters.append(StoreMasterModel.name == store_name)
        if store_id is not None:
            filters.append(ItemSalePredictionModel.store_id == store_id)
        if target_date is not None:
            filters.append(ItemSalePredictionModel.target_date == target_date)
        records = (
            db.query(
                ItemSalePredictionModel,
                ItemMasterModel,
                StoreMasterModel,
            )
            .join(
                ItemMasterModel,
                ItemMasterModel.id == ItemSalePredictionModel.item_id,
                isouter=True,
            )
            .join(
                StoreMasterModel,
                StoreMasterModel.id == ItemSalePredictionModel.store_id,
                isouter=True,
            )
            .filter(and_(*filters))
            .order_by(
                StoreMasterModel.name,
                ItemMasterModel.name,
                ItemSalePredictionModel.target_date,
            )
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [
            ItemSalePrediction(
                id=r.ItemSalePredictionModel.id,
                item_id=r.ItemSalePredictionModel.item_id,
                store_id=r.ItemSalePredictionModel.store_id,
                target_date=r.ItemSalePredictionModel.target_date,
                prediction=r.ItemSalePredictionModel.prediction,
                item_name=r.ItemMasterModel.name,
                store_name=r.StoreMasterModel.name,
                created_at=r.ItemSalePrediction.created_at,
                updated_at=r.ItemSalePrediction.updated_at,
            )
            for r in records
        ]

    def register(
        self,
        db: Session,
        item_sale_prediction: ItemSalePredictionCreate,
        commit: bool = True,
    ) -> Optional[ItemSalePrediction]:
        data = ItemSalePredictionModel(**item_sale_prediction.dict())
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
        item_sale_predictions: List[ItemSalePredictionCreate],
        commit: bool = True,
    ) -> int:
        data = [
            ItemSalePredictionModel(**item_sale_prediction.dict()) for item_sale_prediction in item_sale_predictions
        ]
        db.bulk_save_objects(data)
        if commit:
            db.commit()
            return len(data)
        return 0
