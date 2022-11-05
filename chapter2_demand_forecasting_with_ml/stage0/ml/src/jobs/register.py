import os

import pandas as pd
from src.dataset.schema import WEEKLY_PREDICTION_SCHEMA
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class DataRegister(object):
    def __init__(self):
        pass

    def register(
        self,
        predictions: pd.DataFrame,
        prediction_file_path: str,
    ) -> str:
        predictions = WEEKLY_PREDICTION_SCHEMA.validate(predictions)
        file, ext = os.path.splitext(prediction_file_path)
        if ext != ".csv":
            prediction_file_path = f"{file}.csv"
        logger.info(f"save prediction as csv: {prediction_file_path}")
        predictions.to_csv(prediction_file_path, index=False)
        return prediction_file_path
