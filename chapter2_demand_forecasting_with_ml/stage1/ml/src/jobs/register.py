import os
from datetime import datetime
from typing import List, Optional

import pandas as pd
from src.dataset.data_manager import DBDataManager
from src.dataset.schema import WEEKLY_PREDICTION_SCHEMA, ItemWeeklySalesPredictions
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class DataRegister(object):
    def __init__(
        self,
        db_data_manager: DBDataManager,
    ):
        self.db_data_manager = db_data_manager

    def register(
        self,
        predictions: pd.DataFrame,
        mlflow_experiment_id: Optional[int] = None,
        mlflow_run_id: Optional[str] = None,
    ):
        if mlflow_experiment_id is None or mlflow_run_id is None:
            raise ValueError("mlflow_experiment_id and mlflow_run_id must not be empty")
        self.register_db(
            predictions=predictions,
            mlflow_experiment_id=mlflow_experiment_id,
            mlflow_run_id=mlflow_run_id,
        )

    def register_db(
        self,
        predictions: pd.DataFrame,
        mlflow_experiment_id: int,
        mlflow_run_id: str,
    ):
        predictions = WEEKLY_PREDICTION_SCHEMA.validate(predictions)
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
        self.db_data_manager.insert_item_weekly_sales_predictions(
            item_weekly_sales_predictions=item_weekly_sales_predictions
        )
