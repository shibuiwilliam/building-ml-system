from datetime import date
from typing import List, Optional

from db_client import AbstractDBClient
from model import ItemRepository, ItemSales, ItemSalesRepository, RegionRepository, StoreRepository


class BaseViewModel(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client


class RegionViewModel(BaseViewModel):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.region_repository = RegionRepository(db_client=db_client)

    def list_regions(self) -> List[str]:
        regions = self.region_repository.select()
        region_names = [r.name for r in regions]
        return region_names


class StoreViewModel(BaseViewModel):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.store_repository = StoreRepository(db_client=db_client)

    def list_stores(self) -> List[str]:
        stores = self.store_repository.select()
        store_names = [r.name for r in stores]
        return store_names

    def list_stores_in_region(self, region: str) -> List[str]:
        stores = self.store_repository.select(region=region)
        store_names = [r.name for r in stores]
        return store_names


class ItemViewModel(BaseViewModel):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.item_repository = ItemRepository(db_client=db_client)

    def list_items(self) -> List[str]:
        items = self.item_repository.select()
        item_names = [r.name for r in items]
        return item_names


class ItemSalesViewModel(BaseViewModel):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.item_sales_repository = ItemSalesRepository(db_client=db_client)

    def list_item_sales(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        day_of_week: Optional[str] = None,
        item: Optional[str] = None,
        store: Optional[str] = None,
        region: Optional[str] = None,
    ) -> List[ItemSales]:
        item_sales = []
        limit = 1000
        offset = 0
        while True:
            records = self.item_sales_repository.select(
                date_from=date_from,
                date_to=date_to,
                day_of_week=day_of_week,
                item=item,
                store=store,
                region=region,
                limit=limit,
                offset=offset,
            )
            if len(records) == 0:
                break
            item_sales.extend(records)
        return item_sales
