import os
from datetime import datetime
from typing import List, Optional

import pandas as pd
from src.dataset.data_manager import DATA_SOURCE, DBDataManager
from src.dataset.schema import WEEKLY_PREDICTION_SCHEMA, ItemWeeklySalesPredictions
from src.middleware.db_client import PostgreSQLClient
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
        mlflow_experiment_id: Optional[int] = None,
        mlflow_run_id: Optional[str] = None,
    ):
        if data_source == DATA_SOURCE.LOCAL:
            if prediction_file_path is None:
                raise ValueError("prediction_file_path must not be empty")
            self.register_local(
                predictions=predictions,
                prediction_file_path=prediction_file_path,
            )
        else:
            if mlflow_experiment_id is None or mlflow_run_id is None:
                raise ValueError("mlflow_experiment_id and mlflow_run_id must not be empty")
            self.register_db(
                predictions=predictions,
                mlflow_experiment_id=mlflow_experiment_id,
                mlflow_run_id=mlflow_run_id,
            )

    def register_local(
        self,
        predictions: pd.DataFrame,
        prediction_file_path: str,
    ):
        predictions = WEEKLY_PREDICTION_SCHEMA.validate(predictions)
        file, ext = os.path.splitext(prediction_file_path)
        if ext != ".csv":
            prediction_file_path = f"{file}.csv"
        logger.info(f"save prediction as csv: {prediction_file_path}")
        predictions.to_csv(prediction_file_path, index=False)

    def register_db(
        self,
        predictions: pd.DataFrame,
        mlflow_experiment_id: int,
        mlflow_run_id: str,
    ):
        predictions = WEEKLY_PREDICTION_SCHEMA.validate(predictions)
        db_client = PostgreSQLClient()
        db_data_manager = DBDataManager(db_client=db_client)
        records = predictions.to_dict(orient="records")
        item_weekly_sales_predictions: List[ItemWeeklySalesPredictions] = []
        for r in records:
            item_weekly_sales_predictions.append(
                ItemWeeklySalesPredictions(
                    store=r["store"],
                    item=r["item"],
                    year=int(r["year"]),
                    week_of_year=int(r["week_of_year"]),
                    prediction=float(r["prediction"]),
                    predicted_at=datetime.now().date(),
                    mlflow_experiment_id=mlflow_experiment_id,
                    mlflow_run_id=mlflow_run_id,
                ),
            )
        db_data_manager.insert_item_weekly_sales_predictions(
            item_weekly_sales_predictions=item_weekly_sales_predictions
        )
