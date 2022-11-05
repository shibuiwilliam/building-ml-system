from src.infrastructure.database import AbstractDBClient
from src.middleware.file_reader import read_csv_to_list
from src.middleware.logger import configure_logger
from src.model.region_model import Region
from src.model.store_model import Store
from src.repository.region_repository import RegionRepository
from src.repository.store_repository import StoreRepository
from src.service.abstract_service import AbstractService

logger = configure_logger(__name__)


class StoreService(AbstractService):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.region_repository = RegionRepository(db_client=self.db_client)
        self.store_repository = StoreRepository(db_client=self.db_client)

    def register(
        self,
        region_file_path: str,
        store_file_path: str,
    ):
        self.__register_region(region_file_path=region_file_path)
        self.__register_store(store_file_path=store_file_path)

    def __register_region(
        self,
        region_file_path: str,
    ):
        data = read_csv_to_list(csv_file=region_file_path)
        records = [Region(**d) for d in data]
        for record in records:
            self.region_repository.insert(record=record)

    def __register_store(
        self,
        store_file_path: str,
    ):
        data = read_csv_to_list(csv_file=store_file_path)
        regions = self.region_repository.select()
        region_dict = {r.name: r.id for r in regions}
        for d in data:
            record = Store(
                id=d["id"],
                name=d["name"],
                region_id=region_dict[d["region"]],
            )
            self.store_repository.insert(record=record)
