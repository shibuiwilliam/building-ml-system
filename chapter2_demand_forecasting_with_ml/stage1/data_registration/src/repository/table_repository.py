from src.infrastructure.database import AbstractDBClient
from src.middleware.file_reader import read_text_file
from src.middleware.logger import configure_logger
from src.repository.abstract_repository import BaseRepository

logger = configure_logger(__name__)


class TableRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        BaseRepository.__init__(self, db_client=db_client)

    def create_tables(
        self,
        file_path: str,
    ):
        query = read_text_file(file_path=file_path)
        self.execute_create_query(query=query)
