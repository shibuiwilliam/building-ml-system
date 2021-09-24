import os
from datetime import date, datetime
from typing import List, Optional

import pandas as pd
from pandera import DataFrameSchema
from src.models.dataset import (
    PREDICTION_SCHEMA,
    UPDATED_PREDICTION_SCHEMA,
    load_csv_as_df,
    save_dataframe_to_csv,
    select_and_create_columns,
    select_by_store_and_item,
)
from src.predict.predictor import BasePredictor
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


class PredictionJob(object):
    def __init__(
        self,
        prediction_file_path: str,
        predictor: BasePredictor,
        stores: Optional[List[str]] = None,
        items: Optional[List[str]] = None,
        save_file_directory: str = "/tmp",
        base_schema: DataFrameSchema = PREDICTION_SCHEMA,
        updated_schema: DataFrameSchema = UPDATED_PREDICTION_SCHEMA,
    ):
        self.prediction_file_path = prediction_file_path
        self.predictor = predictor
        self.stores = stores
        self.items = items
        self.base_schema = base_schema
        self.updated_schema = updated_schema
        self.save_file_directory = save_file_directory

    def __get_now(self) -> str:
        return datetime.today().strftime("%Y%m%d_%H%M%S")

    def __make_directory(
        self,
        job_name: str,
        predict_start_date: Optional[date] = None,
        predict_end_date: Optional[date] = None,
    ) -> str:
        logger.info(f"make directory for {predict_start_date} to {predict_end_date}")
        subdirectory = f"{job_name}"

        if predict_start_date is not None:
            _predict_start_date = predict_start_date.strftime("%Y%m%d")
            subdirectory += f"_{_predict_start_date}"
        if predict_end_date is not None:
            _predict_end_date = predict_end_date.strftime("%Y%m%d")
            subdirectory += f"_{_predict_end_date}"

        directory = os.path.join(self.save_file_directory, subdirectory)
        os.makedirs(directory, exist_ok=True)

        logger.info(f"made directory: {directory}")
        return directory

    def __preprocess(
        self,
        directory: str,
    ) -> pd.DataFrame:
        logger.info(f"start preprocess...")
        raw_df = load_csv_as_df(
            file_path=self.prediction_file_path,
            schema=self.base_schema,
        )
        store_item_selected = select_by_store_and_item(
            df=raw_df,
            stores=self.stores,
            items=self.items,
        )
        selected_df = select_and_create_columns(
            df=store_item_selected,
            schema=self.updated_schema,
        )
        save_dataframe_to_csv(
            df=selected_df,
            file_path=os.path.join(directory, f"updated_df_{self.__get_now()}.csv"),
        )
        logger.info(f"done preprocess...")
        return selected_df

    def predict(
        self,
        predict_start_date: Optional[date] = None,
        predict_end_date: Optional[date] = None,
    ):
        logger.info("start prediction...")

        directory = self.__make_directory(
            job_name="prediction",
            predict_start_date=predict_start_date,
            predict_end_date=predict_end_date,
        )
        selected_df = self.__preprocess(directory=directory)

        if predict_start_date is not None:
            selected_df = selected_df[selected_df["date"] >= predict_start_date].reset_index(drop=True)
        if predict_end_date is not None:
            selected_df = selected_df[selected_df["date"] <= predict_end_date].reset_index(drop=True)

        self.predictor.describe()
        predictions = self.predictor.predict(data=selected_df)
        prediction_df = pd.concat(
            [
                predictions.preprocessed_data,
                pd.Series(predictions.predictions),
            ],
            axis=1,
        ).reset_index(drop=True)
        save_dataframe_to_csv(
            df=prediction_df,
            file_path=os.path.join(directory, f"prediction_df_{self.__get_now()}.csv"),
        )
        logger.info("done prediction...")
