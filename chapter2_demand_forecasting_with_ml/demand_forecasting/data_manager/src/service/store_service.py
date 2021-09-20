from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.middleware.file_reader import read_csv_data
from src.middleware.strings import get_uuid
from src.repository.region_master_repository import AbstractRegionMasterRepository, RegionMaster, RegionMasterCreate
from src.repository.store_master_repository import AbstractStoreMasterRepository, StoreMaster, StoreMasterCreate

logger = getLogger(name=__name__)


class AbstractStoreService(ABC):
    def __init__(
        self,
        region_master_repository: AbstractRegionMasterRepository,
        store_master_repository: AbstractStoreMasterRepository,
    ):
        self.region_master_repository = region_master_repository
        self.store_master_repository = store_master_repository

    @abstractmethod
    def initialize_region_master(
        self,
        db: Session,
        file_path: str,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def initialize_store_master(
        self,
        db: Session,
        file_path: str,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def register_region_master(
        self,
        db: Session,
        region_name: Optional[str] = None,
    ) -> Optional[RegionMaster]:
        raise NotImplementedError

    @abstractmethod
    def register_store_master(
        self,
        db: Session,
        store_name: str,
        region_id: Optional[str] = None,
    ) -> Optional[StoreMaster]:
        raise NotImplementedError

    @abstractmethod
    def retrieve_store_master(
        self,
        db: Session,
        id: Optional[str] = None,
        region_id: Optional[str] = None,
        name: Optional[str] = None,
        region_name: Optional[str] = None,
    ) -> List[StoreMaster]:
        raise NotImplementedError


class StoreService(AbstractStoreService):
    def __init__(
        self,
        region_master_repository: AbstractRegionMasterRepository,
        store_master_repository: AbstractStoreMasterRepository,
    ):
        super().__init__(
            region_master_repository=region_master_repository,
            store_master_repository=store_master_repository,
        )

    def initialize_region_master(
        self,
        db: Session,
        file_path: str,
    ) -> int:
        dataset = read_csv_data(file_path=file_path)
        results = []
        for data in dataset:
            result = self.region_master_repository.register(
                db=db,
                region_master=RegionMasterCreate(**data),
                commit=True,
            )
            results.append(result)
        logger.info(f"registered: {results}")
        return len(results)

    def initialize_store_master(
        self,
        db: Session,
        file_path: str,
    ) -> int:
        dataset = read_csv_data(file_path=file_path)
        results = []
        for data in dataset:
            result = self.store_master_repository.register(
                db=db,
                store_master=StoreMasterCreate(**data),
                commit=True,
            )
            results.append(result)
        logger.info(f"registered: {results}")
        return len(results)

    def register_region_master(
        self,
        db: Session,
        region_name: Optional[str] = None,
    ) -> Optional[RegionMaster]:
        result = self.region_master_repository.register(
            db=db,
            region_master=RegionMasterCreate(
                id=get_uuid(),
                name=region_name,
            ),
            commit=True,
        )
        return result

    def register_store_master(
        self,
        db: Session,
        store_name: str,
        region_id: Optional[str] = None,
    ) -> Optional[StoreMaster]:
        result = self.store_master_repository.register(
            db=db,
            store_master=StoreMasterCreate(
                id=get_uuid(),
                region_id=region_id,
                name=store_name,
            ),
            commit=True,
        )
        return result

    def retrieve_store_master(
        self,
        db: Session,
        id: Optional[str] = None,
        region_id: Optional[str] = None,
        name: Optional[str] = None,
        region_name: Optional[str] = None,
    ) -> List[StoreMaster]:
        result = self.store_master_repository.retrieve(
            db=db,
            id=id,
            region_id=region_id,
            name=name,
            region_name=region_name,
        )
        return result
