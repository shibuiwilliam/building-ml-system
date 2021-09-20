from abc import ABC, abstractmethod
from datetime import datetime
from logging import getLogger
from typing import List, Optional

from pydantic import BaseModel, Extra
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
from src.middleware.database import Base
from src.repository.region_master_repository import RegionMasterModel

logger = getLogger(name=__name__)


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
    region_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class AbstractStoreMasterRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def retrieve(
        self,
        db: Session,
        id: Optional[str] = None,
        region_id: Optional[str] = None,
        name: Optional[str] = None,
        region_name: Optional[str] = None,
    ) -> List[StoreMaster]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        db: Session,
        store_master: StoreMasterCreate,
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
        region_name: Optional[str] = None,
    ) -> List[StoreMaster]:
        filters = []
        if id is not None:
            filters.append(StoreMasterModel.id == id)
        if region_id is not None:
            filters.append(StoreMasterModel.region_id == region_id)
        if name is not None:
            filters.append(StoreMasterModel.name == name)
        if region_name is not None:
            filters.append(RegionMasterModel.name == region_name)
        records = (
            db.query(StoreMasterModel, RegionMasterModel)
            .join(
                RegionMasterModel,
                RegionMasterModel.id == StoreMasterModel.region_id,
                isouter=True,
            )
            .filter(and_(*filters))
            .order_by(StoreMasterModel.name)
            .all()
        )
        return [
            StoreMaster(
                id=r.StoreMasterModel.id,
                region_id=r.StoreMasterModel.region_id,
                name=r.StoreMasterModel.name,
                region_name=r.RegionMasterModel.name,
                created_at=r.StoreMasterModel.created_at,
                updated_at=r.StoreMasterModel.updated_at,
            )
            for r in records
        ]

    def register(
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
        data = StoreMasterModel(**store_master.dict())
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
