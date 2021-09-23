import os
from datetime import datetime
from pandera import DataFrameSchema
from src.models.base_model import BaseDemandForecastingModel
from src.models.preprocess import BasePreprocessPipeline
from src.utils.logger import configure_logger
from src.evaluate.evaluator import Evaluator
from src.models.dataset import (
    load_csv_as_df,
    select_and_create_columns,
    save_dataframe_to_csv,
    DAYS_OF_WEEK,
    STORES,
    ITEMS,
    BASE_SCHEMA,
    UPDATED_SCHEMA,
)

logger = configure_logger(__name__)


class TrainJob(object):
    def __init__(
        self,
        data_file_path: str,
        preprocess_pipeline: BasePreprocessPipeline,
        model: BaseDemandForecastingModel,
        evaluator: Evaluator,
        save_file_directory: str = "/tmp",
        base_schema: DataFrameSchema = BASE_SCHEMA,
        updated_schema: DataFrameSchema = UPDATED_SCHEMA,
    ):
        self.data_file_path = data_file_path
        self.preprocess_pipeline = preprocess_pipeline
        self.model = model
        self.evaluator = evaluator
        self.base_schema = base_schema
        self.updated_schema = updated_schema

        self.save_file_directory = save_file_directory
        self.base_file_name = "demand_forecasting"

    def run(self):
        now = datetime.today().strftime("%Y%m%d_%H%M%S")
        self.file_name += f"_{now}"

        self.raw_df = load_csv_as_df(
            file_path=self.data_file_path,
            schema=self.base_schema,
        )
        self.selected_df = select_and_create_columns(
            df=self.raw_df,
            schema=UPDATED_SCHEMA,
        )
        save_dataframe_to_csv(
            df=self.selected_df,
            file_path=os.path.join(self.save_file_directory, f"update_df_{self.file_name}.csv"),
        )
