import asyncio
from datetime import date, datetime
from typing import Dict, List, Optional, Union

import httpx
from data_client.logger import configure_logger
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


class ItemPrice(BaseModel):
    id: str
    item_id: str
    price: int
    applied_from: date
    applied_to: Optional[date]
    item_name: str
    created_at: datetime
    updated_at: datetime


class BaseClient(object):
    def __init__(
        self,
        timeout: int = 10,
        retries: int = 3,
        api_endpoint: str = "http://data_manager:8000/v0",
    ):
        self.api_endpoint = api_endpoint
        self.timeout = timeout
        self.retries = retries
        self.transport = httpx.AsyncHTTPTransport(
            retries=self.retries,
        )
        self.header: Dict[str, str] = {
            "accept": "application/json",
        }


class StoreClient(BaseClient):
    def __init__(
        self,
        timeout: int = 10,
        retries: int = 3,
        api_endpoint: str = "http://data_manager:8000/v0",
    ):
        super().__init__(
            timeout=timeout,
            retries=retries,
            api_endpoint=api_endpoint,
        )
        self.store_master_endpoint = f"{self.api_endpoint}/stores/masters"

    async def async_retrieve(
        self,
        id: Optional[str] = None,
        region_id: Optional[str] = None,
        store_name: Optional[str] = None,
        region_name: Optional[str] = None,
    ) -> List[StoreMaster]:
        async with httpx.AsyncClient(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            params = dict()
            if id is not None:
                params["id"] = id
            if region_id is not None:
                params["region_id"] = region_id
            if store_name is not None:
                params["store_name"] = store_name
            if region_name is not None:
                params["region_name"] = region_name
            r = await client.get(
                url=self.store_master_endpoint,
                params=params,
                headers=self.header,
            )
            if r.status_code != 200:
                return []
            data = r.json()
            if len(data) == 0:
                return []
            result = [StoreMaster(**d) for d in data]
            return result

    def retrieve(
        self,
        id: Optional[str] = None,
        region_id: Optional[str] = None,
        store_name: Optional[str] = None,
        region_name: Optional[str] = None,
    ) -> List[StoreMaster]:
        return asyncio.run(
            self.async_retrieve(
                id=id,
                region_id=region_id,
                store_name=store_name,
                region_name=region_name,
            )
        )


class ItemClient(BaseClient):
    def __init__(
        self,
        timeout: int = 10,
        retries: int = 3,
        api_endpoint: str = "http://data_manager:8000/v0",
    ):
        super().__init__(
            timeout=timeout,
            retries=retries,
            api_endpoint=api_endpoint,
        )
        self.item_master_endpoint = f"{self.api_endpoint}/items/masters"
        self.item_sale_endpoint = f"{self.api_endpoint}/items/sales"
        self.item_price_endpoint = f"{self.api_endpoint}/items/prices"

    async def async_retrieve_item_master(
        self,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
    ) -> List[ItemMaster]:
        async with httpx.AsyncClient(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            params = dict()
            if id is not None:
                params["id"] = id
            if item_name is not None:
                params["item_name"] = item_name
            r = await client.get(
                url=self.item_master_endpoint,
                params=params,
                headers=self.header,
            )
            if r.status_code != 200:
                return []
            data = r.json()
            if len(data) == 0:
                return []
            result = [ItemMaster(**d) for d in data]
            return result

    def retrieve_item_master(
        self,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
    ) -> List[ItemMaster]:
        return asyncio.run(
            self.async_retrieve_item_master(
                id=id,
                item_name=item_name,
            )
        )

    async def async_retrieve_item_price(
        self,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        applied_from: Optional[date] = None,
        applied_to: Optional[date] = None,
    ) -> List[ItemPrice]:
        async with httpx.AsyncClient(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            params = dict()
            if id is not None:
                params["id"] = id
            if item_name is not None:
                params["item_name"] = item_name
            if item_id is not None:
                params["item_id"] = item_id
            if applied_from is not None:
                params["applied_from"] = applied_from
            if applied_to is not None:
                params["applied_to"] = applied_to
            r = await client.get(
                url=self.item_price_endpoint,
                params=params,
                headers=self.header,
            )
            if r.status_code != 200:
                return []
            data = r.json()
            if len(data) == 0:
                return []
            result = [ItemPrice(**d) for d in data]
            return result

    def retrieve_item_price(
        self,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        applied_from: Optional[date] = None,
        applied_to: Optional[date] = None,
    ) -> List[ItemPrice]:
        return asyncio.run(
            self.async_retrieve_item_price(
                id=id,
                item_name=item_name,
                item_id=item_id,
                applied_from=applied_from,
                applied_to=applied_to,
            )
        )

    async def async_retrieve_item_sale(
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
        async with httpx.AsyncClient(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            params: Dict[str, Union[int, str, date]] = dict(
                limit=limit,
                offset=offset,
            )
            if id is not None:
                params["id"] = id
            if item_name is not None:
                params["item_name"] = item_name
            if item_id is not None:
                params["item_id"] = item_id
            if store_name is not None:
                params["store_name"] = store_name
            if store_id is not None:
                params["store_id"] = store_id
            if item_price_id is not None:
                params["item_price_id"] = item_price_id
            if quantity is not None:
                params["quantity"] = quantity
            if sold_at is not None:
                params["sold_at"] = sold_at
            if day_of_week is not None:
                params["day_of_week"] = day_of_week
            r = await client.get(
                url=self.item_sale_endpoint,
                params=params,
                headers=self.header,
            )
            if r.status_code != 200:
                return []
            data = r.json()
            if len(data) == 0:
                return []
            result = [ItemSale(**d) for d in data]
            return result

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
        return asyncio.run(
            self.async_retrieve_item_sale(
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
        )
