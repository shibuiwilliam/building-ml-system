import os
from datetime import date, datetime
from typing import Dict, Optional

import pandas as pd
from pandera import DataFrameSchema
from src.evaluate.evaluator import Evaluator
from src.models.base_model import BaseDemandForecastingModel
from src.models.dataset import (
    BASE_SCHEMA,
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

        self.evaluator: Optional[Evaluator] = None

    def __make_directory(
        self,
        job_name: str,
        train_start_date: date,
        train_end_date: date,
        test_start_date: Optional[date] = None,
        test_end_date: Optional[date] = None,
    ) -> str:
        logger.info(
            f"make directory for {train_start_date} to {train_end_date} and {test_start_date} to {test_end_date}"
        )
        _train_start_date = train_start_date.strftime("%Y%m%d")
        _train_end_date = train_end_date.strftime("%Y%m%d")
        subdirectory = f"{job_name}_{_train_start_date}_{_train_end_date}"

        if test_start_date is not None:
            _test_start_date = test_start_date.strftime("%Y%m%d")
            subdirectory += f"_{_test_start_date}"
        if test_end_date is not None:
            _test_end_date = test_end_date.strftime("%Y%m%d")
            subdirectory += f"_{_test_end_date}"

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
            file_path=self.data_file_path,
            schema=self.base_schema,
        )
        selected_df = select_and_create_columns(
            df=raw_df,
            schema=UPDATED_SCHEMA,
        )
        save_dataframe_to_csv(
            df=selected_df,
            file_path=os.path.join(directory, f"update_df_{self.__get_now()}.csv"),
        )

        preprocessed_array = self.preprocess_pipeline.fit_transform(x=selected_df)
        preprocessed_df = self.preprocess_pipeline.to_dataframe(
            base_dataframe=selected_df,
            x=preprocessed_array,
        )
        save_dataframe_to_csv(
            df=preprocessed_df,
            file_path=os.path.join(directory, f"preprocessed_df_{self.__get_now()}.csv"),
        )
        self.preprocess_pipeline.dump_pipeline(
            file_path=os.path.join(directory, f"preprocess_pipeline_{self.__get_now()}.pkl")
        )
        logger.info(f"done preprocess...")
        return preprocessed_df

    def __get_now(self) -> str:
        return datetime.today().strftime("%Y%m%d_%H%M%S")

    def experiment(
        self,
        train_start_date: date,
        train_end_date: date,
        test_start_date: date,
        test_end_date: date,
        model_params: Dict,
    ):
        logger.info("start experiment...")

        directory = self.__make_directory(
            job_name="experiment",
            train_start_date=train_start_date,
            train_end_date=train_end_date,
            test_start_date=test_start_date,
            test_end_date=test_end_date,
        )

        preprocessed_df = self.__preprocess(directory=directory)

        self.train_df, self.test_df = self.preprocess_pipeline.train_test_split_by_date(
            preprocessed_df=preprocessed_df,
            train_start_date=train_start_date,
            train_end_date=train_end_date,
            test_start_date=test_start_date,
            test_end_date=test_end_date,
        )
        save_dataframe_to_csv(
            df=self.train_df,
            file_path=os.path.join(directory, f"train_df_{self.__get_now()}.csv"),
        )
        save_dataframe_to_csv(
            df=self.test_df,
            file_path=os.path.join(directory, f"test_df_{self.__get_now()}.csv"),
        )

        x_train = self.train_df.drop(["date", "store", "item", "sales"], axis=1)
        y_train = self.train_df.sales

        x_test = self.test_df.drop(["date", "store", "item", "sales"], axis=1)
        y_test = self.test_df.sales

        self.model.params = model_params
        evals_result = self.model.train(
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
        )
        self.model.save_model_params(
            file_path=os.path.join(directory, f"{self.model.name}_params_{self.__get_now()}.json")
        )
        self.model.save_train_history(
            evals_result=evals_result,
            file_path=os.path.join(directory, f"{self.model.name}_train_history_{self.__get_now()}.json"),
        )
        self.model.save(file_path=os.path.join(directory, f"{self.model.name}_{self.__get_now()}.txt"))
        logp1_predictions = self.model.predict(x_test=x_test)

        sales = self.preprocess_pipeline.inverse_transform_target(y=y_test)
        predictions = self.preprocess_pipeline.inverse_transform_target(y=logp1_predictions)

        self.evaluator = Evaluator(
            dates=self.test_df.date,
            stores=self.test_df.store,
            items=self.test_df.item,
            true_sales=sales,
            predicted_sales=predictions,
            absolute=False,
        )
        self.evaluator.save_date_based_results(
            file_path=os.path.join(directory, f"{self.model.name}_date_based_results_{self.__get_now()}.csv")
        )
        self.evaluator.save_week_based_results(
            file_path=os.path.join(directory, f"{self.model.name}_week_based_results_{self.__get_now()}.csv")
        )
        logger.info("done experiment...")

    def train(
        self,
        train_start_date: date,
        train_end_date: date,
        model_params: Dict,
    ):
        logger.info("start train...")

        directory = self.__make_directory(
            job_name="train",
            train_start_date=train_start_date,
            train_end_date=train_end_date,
            test_start_date=None,
            test_end_date=None,
        )

        preprocessed_df = self.__preprocess(directory=directory)

        x_train = preprocessed_df.drop(["date", "store", "item", "sales"], axis=1)
        y_train = preprocessed_df.sales

        self.model.params = model_params
        evals_result = self.model.train(
            x_train=x_train,
            y_train=y_train,
            x_test=None,
            y_test=None,
        )
        self.model.save_model_params(
            file_path=os.path.join(directory, f"{self.model.name}_params_{self.__get_now()}.json")
        )
        self.model.save_train_history(
            evals_result=evals_result,
            file_path=os.path.join(directory, f"{self.model.name}_train_history_{self.__get_now()}.json"),
        )
        self.model.save(file_path=os.path.join(directory, f"{self.model.name}_{self.__get_now()}.txt"))
        self.model.save_as_onnx(file_path=os.path.join(directory, f"{self.model.name}_{self.__get_now()}.onnx"))

        logger.info("done train...")
