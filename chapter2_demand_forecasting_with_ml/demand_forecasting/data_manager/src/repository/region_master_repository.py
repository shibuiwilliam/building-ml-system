from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra
from sqlalchemy import Column, DateTime, String, Text, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp
from src.middleware.logger import configure_logger
from src.repository.db import Base

logger = configure_logger(name=__name__)


class RegionMasterModel(Base):
    __tablename__ = "region_master"

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


class RegionMasterBase(BaseModel):
    id: str
    name: str


class RegionMasterCreate(RegionMasterBase):
    pass

    class Config:
        extra = Extra.forbid


class RegionMaster(RegionMasterBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class AbstractRegionMasterRepository(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def retrieve(
        self,
        db: Session,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> List[RegionMaster]:
        raise NotImplementedError

    @abstractmethod
    def record(
        self,
        db: Session,
        region_master: RegionMasterCreate,
        commit: bool = True,
    ) -> Optional[RegionMaster]:
        raise NotImplementedError


class RegionMasterRepository(AbstractRegionMasterRepository):
    def __init__(self):
        pass

    def retrieve(
        self,
        db: Session,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> List[RegionMaster]:
        filters = []
        if id is not None:
            filters.append(RegionMasterModel.id == id)
        if name is not None:
            filters.append(RegionMasterModel.name == name)
        records = db.query(RegionMasterModel).filter(and_(*filters)).order_by(RegionMasterModel.name).all()
        return [
            RegionMaster(
                id=r.id,
                name=r.name,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in records
        ]

    def record(
        self,
        db: Session,
        region_master: RegionMasterCreate,
        commit: bool = True,
    ) -> Optional[RegionMaster]:
        is_exists = self.retrieve(
            db=db,
            name=region_master.name,
        )
        if len(is_exists) > 0:
            return is_exists[0]
        data = RegionMasterModel(
            id=region_master.id,
            name=region_master.name,
        )
        db.add(data)
        if commit:
            db.commit()
            db.refresh(data)
            return RegionMaster(
                id=data.id,
                name=data.name,
                created_at=data.created_at,
                updated_at=data.updated_at,
            )
        return None
