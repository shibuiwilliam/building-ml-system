from time import sleep
from typing import Dict, List

import pandas as pd
from configurations import Configurations
from logger import configure_logger
from model import ItemMaster, ItemRepository, ItemSale, StoreMaster, StoreRepository
from pydantic import BaseModel

logger = configure_logger(__name__)


class StoreViewModel(object):
    def __init__(self):
        self.store_repository = StoreRepository(
            timeout=10,
            retries=3,
            api_endpoint=Configurations.api_endpoint,
        )
        self.store_master_list: List[StoreMaster] = []
        self.region_masters: List[str] = []
        self.store_masters: List[str] = []
        self.store_to_region: Dict[str, str] = {}
        self.__init_store_masters()

    def __init_store_masters(self):
        logger.info(f"initialize store master data")
        while True:
            if self.store_repository.ping():
                break
            sleep(10)
        self.store_master_list = self.store_repository.retrieve()
        region_masters = []
        store_masters = []
        store_to_region = {}
        for store_master in self.store_master_list:
            region_masters.append(store_master.region_name)
            store_masters.append(store_master.name)
            store_to_region[store_master.name] = store_master.region_name
        self.region_masters = list(set(region_masters))
        self.store_masters = list(set(store_masters))
        self.store_to_region = store_to_region
        logger.info(f"initialized store master data")

    def region_of_store(self, store: str) -> str:
        return self.store_to_region[store]


class ItemViewModel(object):
    def __init__(self):
        self.item_repository = ItemRepository(
            timeout=10,
            retries=3,
            api_endpoint=Configurations.api_endpoint,
        )
        self.item_master_list: List[ItemMaster] = []
        self.item_masters: List[str] = []
        self.item_sales: List[ItemSale] = []
        self.__init_item_masters()

    def __init_item_masters(self):
        logger.info(f"initialize item master data")
        while True:
            if self.item_repository.ping():
                break
            sleep(10)
        self.item_master_list = self.item_repository.retrieve_item_master()
        item_masters = []
        for item_master in self.item_master_list:
            item_masters.append(item_master.name)
        self.item_masters = item_masters
        logger.info(f"initialized item master data")


class Quantities(BaseModel):
    dates: List[str]
    day_of_weeks: List[str]
    quantities: List[int]
    total_sales: List[int]


class ItemSaleViewModel(object):
    def __init__(self):
        self.item_repository = ItemRepository(
            timeout=10,
            retries=3,
            api_endpoint=Configurations.api_endpoint,
        )
        self.item_sales_list: List[ItemSale] = []
        self.item_sales_df: pd.DataFrame = None
        self.__init_item_sale()

    def __init_item_sale(self):
        logger.info(f"initialize item sale data")
        while True:
            if self.item_repository.ping():
                break
            sleep(10)
        limit = 1000
        offset = 0
        while True:
            item_sales = self.item_repository.retrieve_item_sale(limit=limit, offset=offset)
            if len(item_sales) == 0:
                break
            self.item_sales_list.extend(item_sales)
            offset += limit
        item_sales_column = list(self.item_sales_list[0].dict().keys())
        _item_sales_list = [list(item_sale.dict().values()) for item_sale in self.item_sales_list]
        self.item_sales_df = pd.DataFrame(_item_sales_list, columns=item_sales_column).sort_values(
            by=["store_name", "item_name", "sold_at"]
        )
        logger.info(f"initialized item sale data")

    def quantity_by_store_item(self, store_name: str, item_name: str) -> Quantities:
        df = self.item_sales_df[self.item_sales_df["store_name"] == store_name][
            self.item_sales_df["item_name"] == item_name
        ].sort_values(by=["sold_at"])
        quantities = Quantities(
            dates=[],
            day_of_weeks=[],
            quantities=[],
            total_sales=[],
        )
        for data in df.to_dict("records"):
            quantities.dates.append(data["sold_at"])
            quantities.day_of_weeks.append(data["day_of_week"])
            quantities.quantities.append(data["quantity"])
            quantities.total_sales.append(data["total_sales"])
        return quantities
