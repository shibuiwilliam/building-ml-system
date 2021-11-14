import os
from typing import Optional

import pandas as pd
from omegaconf import DictConfig
from src.dataset.data_manager import DATA_SOURCE, DBDataManager
from src.middleware.db_client import DBClient
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class DataRegister(object):
    def __init__(self):
        pass

    def register(
        self,
        predictions: pd.DataFrame,
        data_source: DATA_SOURCE = DATA_SOURCE.LOCAL,
        prediction_file_path: Optional[str] = None,
    ):
        if data_source == DATA_SOURCE.LOCAL:
            self.register_local(
                predictions=predictions,
                prediction_file_path=prediction_file_path,
            )
        else:
            self.register_db(predictions=predictions)

    def register_local(
        self,
        predictions: pd.DataFrame,
        prediction_file_path: str,
    ):
        file, ext = os.path.splitext(prediction_file_path)
        if ext != ".csv":
            prediction_file_path = f"{file}.csv"
        logger.info(f"save prediction as csv: {prediction_file_path}")
        predictions.to_csv(prediction_file_path, index=False)

    def register_db(
        self,
        predictions: pd.DataFrame,
    ):
        db_client = DBClient()
        db_data_manager = DBDataManager(db_client=db_client)
        db_data_manager.insert_item_sales_predictions(predictions=predictions)
