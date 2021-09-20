from abc import ABC, abstractmethod
from datetime import datetime
from logging import getLogger
from typing import List, Optional

from pydantic import BaseModel, Extra
from sqlalchemy import Column, DateTime, String, Text, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
from src.middleware.database import Base

logger = getLogger(name=__name__)


class ItemMasterModel(Base):
    __tablename__ = "item_master"

    id = Column(
        String(32),
        nullable=False,
        primary_key=True,
    )
    name = Column(
        Text,
        nullable=False,
        unique=True,
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


class ItemMasterBase(BaseModel):
    id: str
    name: str


class ItemMasterCreate(ItemMasterBase):
    pass

    class Config:
        extra = Extra.forbid


class ItemMaster(ItemMasterBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class AbstractItemMasterRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def retrieve(
        self,
        db: Session,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> List[ItemMaster]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        db: Session,
        item_master: ItemMasterCreate,
        commit: bool = True,
    ) -> Optional[ItemMaster]:
        raise NotImplementedError


class ItemMasterRepository(AbstractItemMasterRepository):
    def __init__(self):
        pass

    def retrieve(
        self,
        db: Session,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> List[ItemMaster]:
        filters = []
        if id is not None:
            filters.append(ItemMasterModel.id == id)
        if name is not None:
            filters.append(ItemMasterModel.name == name)
        records = db.query(ItemMasterModel).filter(and_(*filters)).order_by(ItemMasterModel.name).all()
        return [
            ItemMaster(
                id=r.id,
                name=r.name,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in records
        ]

    def register(
        self,
        db: Session,
        item_master: ItemMasterCreate,
        commit: bool = True,
    ) -> Optional[ItemMaster]:
        is_exists = self.retrieve(
            db=db,
            name=item_master.name,
        )
        if len(is_exists) > 0:
            return is_exists[0]
        data = ItemMasterModel(**item_master.dict())
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
