from src.configurations import Configurations
from src.middleware.database import AbstractDBClient
from src.middleware.file_reader import read_csv_to_list
from src.middleware.logger import configure_logger
from src.model.region_model import Region
from src.repository.region_repository import RegionQuery, RegionRepository
from src.service.abstract_service import AbstractService

logger = configure_logger(__name__)


class StoreService(AbstractService):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.region_repository = RegionRepository(db_client=self.db_client)

    def register(self):
        self.__register_region()

    def __register_region(self):
        data = read_csv_to_list(csv_file=Configurations.region_file_path)
        records = [Region(**d) for d in data]
        for record in records:
            self.region_repository.insert(record=record)
