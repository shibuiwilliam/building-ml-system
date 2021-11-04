from datetime import datetime

from src.configurations import Configurations
from src.middleware.database import AbstractDBClient
from src.middleware.file_reader import read_csv_to_list
from src.middleware.logger import configure_logger
from src.model.item_model import Item
from src.model.item_price_model import ItemPrice
from src.repository.item_price_repository import ItemPriceRepository
from src.repository.item_repository import ItemQuery, ItemRepository
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

    def register(self):
        self.__register_item()
        self.__register_item_price()

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
