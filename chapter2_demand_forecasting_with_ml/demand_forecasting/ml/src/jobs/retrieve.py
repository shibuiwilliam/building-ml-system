from src.dataset.data_manager import DATA_SOURCE, load_df_from_csv, DBDataManager
from src.dataset.schema import BASE_SCHEMA
from omegaconf import DictConfig
from src.models.preprocess import DataPreprocessPipeline, WeekBasedSplit
from src.middleware.db_client import DBClient
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class DataRetriever(object):
    def __init__(self):
        pass

    def retrieve_dataset(
        self,
        cfg: DictConfig,
        data_source: DATA_SOURCE = DATA_SOURCE.LOCAL,
    ):
        if data_source == DATA_SOURCE.LOCAL:
            raw_df = load_df_from_csv(file_path=cfg.jobs.data.path)
        elif data_source == DATA_SOURCE.DB:
            db_client = DBClient()
            db_data_manager = DBDataManager(db_client=db_client)
        else:
            raise ValueError
