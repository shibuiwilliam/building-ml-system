from datetime import datetime

from src.configurations import Configurations
from src.middleware.database import AbstractDBClient
from src.middleware.file_reader import read_csv_to_list
from src.middleware.logger import configure_logger
from src.middleware.strings import get_uuid
from src.model.item_model import Item
from src.model.item_price_model import ItemPrice
from src.model.item_sales_model import ItemSales
from src.repository.item_price_repository import ItemPriceRepository
from src.repository.item_repository import ItemQuery, ItemRepository
from src.repository.item_sales_repository import ItemSalesRepository
from src.repository.store_repository import StoreRepository
from src.service.abstract_service import AbstractService

logger = configure_logger(__name__)


class ItemService(AbstractService):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.item_repository = ItemRepository(db_client=self.db_client)
        self.item_price_repository = ItemPriceRepository(db_client=self.db_client)
        self.item_sales_repository = ItemSalesRepository(db_client=self.db_client)
        self.store_repository = StoreRepository(db_client=self.db_client)

    def register(self):
        self.__register_item()
        self.__register_item_price()
        self.__register_item_sales()

    def __register_item(self):
        data = read_csv_to_list(csv_file=Configurations.item_file_path)
        records = [Item(**d) for d in data]
        for record in records:
            self.item_repository.insert(record=record)

    def __register_item_price(self):
        data = read_csv_to_list(csv_file=Configurations.item_price_path)
        items = self.item_repository.select()
        item_dict = {i.name: i.id for i in items}
        for d in data:
            record = ItemPrice(
                id=d["id"],
                item_id=item_dict[d["item_name"]],
                price=int(d["price"]),
                applied_from=datetime.strptime(d["applied_from"], "%Y-%m-%d").date(),
                applied_to=datetime.strptime(d["applied_to"], "%Y-%m-%d").date(),
            )
            self.item_price_repository.insert(record=record)

    def __register_item_sales(self):
        data = read_csv_to_list(csv_file=Configurations.item_sale_records_2017_2019_path)
        stores = self.store_repository.select()
        store_dict = {s.name: s.id for s in stores}
        items = self.item_repository.select()
        item_dict = {i.name: i.id for i in items}
        item_prices = self.item_price_repository.select()
        item_price_dict = {i.item_id: i.id for i in item_prices}

        limit = 1000
        i = 0
        records = []
        while i < len(data):
            d = data[i]
            item_id = item_dict[d["item"]]
            item_price_id = item_price_dict[item_id]
            records.append(
                ItemSales(
                    id=get_uuid(),
                    date=datetime.strptime(d["date"], "%Y-%m-%d").date(),
                    day_of_week=d["day_of_week"],
                    store_id=store_dict[d["store"]],
                    item_id=item_id,
                    item_price_id=item_price_id,
                    sales=int(d["sales"]),
                    total_sales_amount=int(d["total_sales_amount"]),
                )
            )
            i += 1
            if i % limit == 0:
                self.item_sales_repository.bulk_insert(records=records)
                records = []
                logger.info(f"registered {i} item sales...")
        if len(records) > 0:
            self.item_sales_repository.bulk_insert(records=records)
