from datetime import date, datetime
from typing import List, Optional

from configurations import Configurations
from data_client.data_client import ItemClient, StoreClient
from logger import configure_logger
from pydantic import BaseModel

logger = configure_logger(__name__)


class StoreMaster(BaseModel):
    id: str
    region_id: str
    name: str
    region_name: str
    created_at: datetime
    updated_at: datetime


class ItemMaster(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime


class ItemSale(BaseModel):
    id: str
    item_id: str
    store_id: str
    item_price_id: str
    quantity: int
    total_sales: int
    sold_at: date
    day_of_week: str
    item_name: str
    store_name: str
    price: int
    created_at: datetime
    updated_at: datetime


class BaseRepository(object):
    def __init__(
        self,
        timeout: int = 10,
        retries: int = 3,
        api_endpoint: str = Configurations.api_endpoint,
    ):
        self.api_endpoint = api_endpoint
        self.timeout = timeout
        self.retries = retries


class StoreRepository(BaseRepository):
    def __init__(
        self,
        timeout: int = 10,
        retries: int = 3,
        api_endpoint: str = Configurations.api_endpoint,
    ):
        super().__init__(
            timeout=timeout,
            retries=retries,
            api_endpoint=api_endpoint,
        )
        self.store_client = StoreClient(
            timeout=self.timeout,
            retries=self.retries,
            api_endpoint=self.api_endpoint,
        )

    def ping(self) -> bool:
        logger.info("send ping...")
        response = self.store_client.ping()
        return response

    def retrieve(
        self,
        id: Optional[str] = None,
        region_id: Optional[str] = None,
        store_name: Optional[str] = None,
        region_name: Optional[str] = None,
    ) -> List[StoreMaster]:
        response = self.store_client.retrieve(
            id=id,
            region_id=region_id,
            store_name=store_name,
            region_name=region_name,
        )
        stores = [StoreMaster(**r.dict()) for r in response]
        return stores


class ItemRepository(BaseRepository):
    def __init__(
        self,
        timeout: int = 10,
        retries: int = 3,
        api_endpoint: str = Configurations.api_endpoint,
    ):
        super().__init__(
            timeout=timeout,
            retries=retries,
            api_endpoint=api_endpoint,
        )
        self.item_client = ItemClient(
            timeout=self.timeout,
            retries=self.retries,
            api_endpoint=self.api_endpoint,
        )

    def ping(self) -> bool:
        logger.info("send ping...")
        response = self.item_client.ping()
        return response

    def retrieve_item_master(
        self,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
    ) -> List[ItemMaster]:
        response = self.item_client.retrieve_item_master(
            id=id,
            item_name=item_name,
        )
        item_masters = [ItemMaster(**r.dict()) for r in response]
        return item_masters

    def retrieve_item_sale(
        self,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        store_name: Optional[str] = None,
        store_id: Optional[str] = None,
        item_price_id: Optional[str] = None,
        quantity: Optional[int] = None,
        sold_at: Optional[date] = None,
        day_of_week: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ItemSale]:
        response = self.item_client.retrieve_item_sale(
            id=id,
            item_name=item_name,
            item_id=item_id,
            store_name=store_name,
            store_id=store_id,
            item_price_id=item_price_id,
            quantity=quantity,
            sold_at=sold_at,
            day_of_week=day_of_week,
            limit=limit,
            offset=offset,
        )
        item_masters = [ItemSale(**r.dict()) for r in response]
        return item_masters
