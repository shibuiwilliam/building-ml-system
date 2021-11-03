from src.configurations import Configurations
from src.middleware.database import AbstractDBClient
from src.middleware.logger import configure_logger
from src.repository.table_repository import TableRepository
from src.service.abstract_service import AbstractService

logger = configure_logger(__name__)


class TableService(AbstractService):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.table_repository = TableRepository(db_client=self.db_client)

    def register(self):
        self.table_repository.create_tables(file_path=Configurations.create_sql_file_path)
