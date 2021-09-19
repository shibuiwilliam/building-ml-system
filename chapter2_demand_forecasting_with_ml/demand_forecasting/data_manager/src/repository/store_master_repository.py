from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Text, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
from src.middleware.logger import configure_logger
from src.repository.db import Base

logger = configure_logger(name=__name__)


class StoreMasterModel(Base):
    __tablename__ = "store_master"

    id = Column(
        String(32),
        nullable=False,
        primary_key=True,
    )
    region_id = Column(
        String(32),
        ForeignKey("region_master.id"),
        nullable=False,
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


class StoreMasterBase(BaseModel):
    id: str
    region_id: str
    name: str


class StoreMasterCreate(StoreMasterBase):
    pass


class StoreMaster(StoreMasterBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class AbstractStoreMasterRepository(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def retrieve(
        self,
        db: Session,
        id: Optional[str] = None,
        region_id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> List[StoreMaster]:
        raise NotImplementedError

    @abstractmethod
    def record(
        self,
        db: Session,
        region_master: StoreMasterCreate,
        commit: bool = True,
    ) -> Optional[StoreMaster]:
        raise NotImplementedError


class StoreMasterRepository(AbstractStoreMasterRepository):
    def __init__(self):
        pass

    def retrieve(
        self,
        db: Session,
        id: Optional[str] = None,
        region_id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> List[StoreMaster]:
        filters = []
        if id is not None:
            filters.append(StoreMasterModel.id == id)
        if region_id is not None:
            filters.append(StoreMasterModel.region_id == region_id)
        if name is not None:
            filters.append(StoreMasterModel.name == name)
        records = db.query(StoreMasterModel).filter(and_(*filters)).order_by(StoreMasterModel.name).all()
        return [
            StoreMaster(
                id=r.id,
                region_id=r.region_id,
                name=r.name,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in records
        ]

    def record(
        self,
        db: Session,
        store_master: StoreMasterCreate,
        commit: bool = True,
    ) -> Optional[StoreMaster]:
        is_exists = self.retrieve(
            db=db,
            name=store_master.name,
        )
        if len(is_exists) > 0:
            return is_exists[0]
        data = StoreMasterModel(
            id=store_master.id,
            region_id=store_master.region_id,
            name=store_master.name,
        )
        db.add(data)
        if commit:
            db.commit()
            db.refresh(data)
            return StoreMaster(
                id=data.id,
                region_id=data.region_id,
                name=data.name,
                created_at=data.created_at,
                updated_at=data.updated_at,
            )
        return None
