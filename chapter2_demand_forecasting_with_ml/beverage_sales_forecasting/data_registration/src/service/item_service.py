from datetime import datetime, timedelta, date
from src.middleware.database import AbstractDBClient
from src.middleware.file_reader import read_csv_to_list
from src.middleware.logger import configure_logger
from src.middleware.strings import get_uuid
from src.model.item_model import Item
from src.model.item_price_model import ItemPrice, ItemPriceUpdate
from src.model.item_sales_model import ItemSales
from src.repository.item_price_repository import ItemPriceQuery, ItemPriceRepository
from src.repository.item_repository import ItemRepository
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

    def register(
        self,
        item_file_path: str,
        item_price_path: str,
    ):
        self.__register_item(item_file_path=item_file_path)
        self.__register_item_price(item_price_path=item_price_path)

    def register_records(
        self,
        item_sales_records_path: str,
    ):
        self.__register_item_sales(item_sales_records_path=item_sales_records_path)

    def __register_item(
        self,
        item_file_path: str,
    ):
        data = read_csv_to_list(csv_file=item_file_path)
        records = [Item(**d) for d in data]
        for record in records:
            self.item_repository.insert(record=record)

    def __register_item_price(
        self,
        item_price_path: str,
    ):
        data = read_csv_to_list(csv_file=item_price_path)
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

    def __register_item_sales(
        self,
        item_sales_records_path: str,
    ):
        data = read_csv_to_list(csv_file=item_sales_records_path)

        stores = self.store_repository.select()
        store_dict = {s.name: s.id for s in stores}

        items = self.item_repository.select()
        item_dict = {i.name: i.id for i in items}

        item_prices = self.item_price_repository.select()
        item_price_dict = {
            i.item_id: {
                d: i.id
                for d in [i.applied_from + timedelta(days=x) for x in range((i.applied_to - i.applied_from).days + 1)]
            }
            for i in item_prices
        }

        limit = 1000
        i = 0
        records = []
        while i < len(data):
            d = data[i]
            sales_date = datetime.strptime(d["date"], "%Y-%m-%d").date()
            item_id = item_dict[d["item"]]
            item_price_id = item_price_dict[item_id][sales_date]
            records.append(
                ItemSales(
                    id=get_uuid(),
                    date=sales_date,
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

    def register_new_item_price(
        self,
        item_id: str,
        price: int,
        applied_from: date,
    ):
        applie_to = date(2099, 12, 31)
        new_item_price = ItemPrice(
            id=get_uuid(),
            item_id=item_id,
            price=price,
            applied_from=applied_from,
            applie_to=applie_to,
        )
        self.item_price_repository.insert(record=new_item_price)

        current_item_prices = self.item_price_repository.select(
            condition=ItemPriceQuery(
                item_ids=[item_id],
                applied_at=applie_to,
            ),
        )
        if len(current_item_prices) > 0:
            current_item_price = current_item_prices[0]
            self.item_price_repository.update(
                record=ItemPriceUpdate(
                    id=current_item_price.id,
                    applie_to=applied_from,
                ),
            )
