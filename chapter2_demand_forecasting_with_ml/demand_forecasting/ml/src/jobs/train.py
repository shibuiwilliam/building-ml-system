import os
from datetime import date, datetime
from typing import Dict, Optional

import pandas as pd
from pandera import DataFrameSchema
from src.evaluate.evaluator import Evaluator
from src.models.base_model import BaseDemandForecastingModel
from src.models.dataset import (
    BASE_SCHEMA,
    DAYS_OF_WEEK,
    ITEMS,
    STORES,
    UPDATED_SCHEMA,
    load_csv_as_df,
    save_dataframe_to_csv,
    select_and_create_columns,
)
from src.models.preprocess import BasePreprocessPipeline
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


class TrainJob(object):
    def __init__(
        self,
        data_file_path: str,
        preprocess_pipeline: BasePreprocessPipeline,
        model: BaseDemandForecastingModel,
        save_file_directory: str = "/tmp",
        base_schema: DataFrameSchema = BASE_SCHEMA,
        updated_schema: DataFrameSchema = UPDATED_SCHEMA,
    ):
        self.data_file_path = data_file_path
        self.preprocess_pipeline = preprocess_pipeline
        self.model = model
        self.base_schema = base_schema
        self.updated_schema = updated_schema

        self.save_file_directory = save_file_directory
        self.base_file_name = "demand_forecasting"

        self.file_name: str = ""
        self.raw_df: Optional[pd.DataFrame] = None
        self.selected_df: Optional[pd.DataFrame] = None
        self.preprocessed_df: Optional[pd.DataFrame] = None
        self.train_df: Optional[pd.DataFrame] = None
        self.test_df: Optional[pd.DataFrame] = None

        self.evaluator: Optional[Evaluator] = None

    def experiment(
        self,
        train_start_date: date,
        train_end_date: date,
        test_start_date: date,
        test_end_date: date,
        train_params: Dict,
    ):
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

        preprocessed_array = self.preprocess_pipeline.fit_transform(x=self.selected_df)
        self.preprocessed_df = self.preprocess_pipeline.to_dataframe(
            base_dataframe=self.selected_df,
            x=preprocessed_array,
        )
        save_dataframe_to_csv(
            df=self.preprocessed_df,
            file_path=os.path.join(self.save_file_directory, f"preprocessed_df_{self.file_name}.csv"),
        )
        self.train_df, self.test_df = self.preprocess_pipeline.train_test_split_by_date(
            preprocessed_df=self.preprocessed_df,
            train_start_date=train_start_date,
            train_end_date=train_end_date,
            test_start_date=test_start_date,
            test_end_date=test_end_date,
        )
        save_dataframe_to_csv(
            df=self.train_df,
            file_path=os.path.join(self.save_file_directory, f"train_df_{self.file_name}.csv"),
        )
        save_dataframe_to_csv(
            df=self.test_df,
            file_path=os.path.join(self.save_file_directory, f"test_df_{self.file_name}.csv"),
        )
        self.preprocess_pipeline.dump_pipeline(
            file_path=os.path.join(self.save_file_directory, f"preprocess_pipeline_{self.file_name}.pkl")
        )

        x_train = self.train_df.drop(["date", "store", "item", "sales"])
        x_test = self.test_df.drop(["date", "store", "item", "sales"])
        y_train = self.train_df[["date", "store", "item", "sales"]]
        y_test = self.test_df[["date", "store", "item", "sales"]]

        self.model.params = train_params
        self.model.train(
            x_train=x_train,
            x_test=x_test,
            y_train=y_train["sales"],
            y_test=y_test["sales"],
        )
        self.model.save(file_path=os.path.join(self.save_file_directory, f"{self.model.name}_{self.file_name}.txt"))
        self.model.save_as_onnx(
            file_path=os.path.join(self.save_file_directory, f"{self.model.name}_{self.file_name}.onnx")
        )
        predictions = self.model.predict(x_test=x_test)

        self.evaluator = Evaluator(
            dates=self.test_df["dates"],
            stores=self.test_df["store"],
            items=self.test_df["item"],
            true_sales=self.test_df["sales"],
            predicted_sales=predictions,
            absolute=False,
        )
        self.evaluator.save_date_based_results(
            file_path=os.path.join(
                self.save_file_directory, f"{self.model.name}_date_based_results_{self.file_name}.csv"
            )
        )
        self.evaluator.save_week_based_results(
            file_path=os.path.join(
                self.save_file_directory, f"{self.model.name}_week_based_results_{self.file_name}.csv"
            )
        )
