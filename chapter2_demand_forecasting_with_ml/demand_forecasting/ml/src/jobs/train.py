import os
from datetime import date, datetime
from typing import Dict, List, Optional, Union

import numpy as np
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
    select_by_store_and_item,
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
        stores: Optional[List[str]] = None,
        items: Optional[List[str]] = None,
        save_file_directory: str = "/tmp",
        base_schema: DataFrameSchema = BASE_SCHEMA,
        updated_schema: DataFrameSchema = UPDATED_SCHEMA,
    ):
        self.data_file_path = data_file_path
        self.preprocess_pipeline = preprocess_pipeline
        self.model = model
        self.stores = stores
        self.items = items
        self.base_schema = base_schema
        self.updated_schema = updated_schema
        self.save_file_directory = save_file_directory
        self.onnx_file_path = ""

    def __get_now(self) -> str:
        return datetime.today().strftime("%Y%m%d_%H%M%S")

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

    def __make_model(
        self,
        directory: str,
        model_params: Dict,
        x_train: Union[np.ndarray, pd.DataFrame],
        y_train: Union[np.ndarray, pd.DataFrame],
        x_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        y_test: Optional[Union[np.ndarray, pd.DataFrame]] = None,
    ):
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

        train_df, test_df = self.preprocess_pipeline.train_test_split_by_date(
            preprocessed_df=preprocessed_df,
            train_start_date=train_start_date,
            train_end_date=train_end_date,
            test_start_date=test_start_date,
            test_end_date=test_end_date,
        )
        save_dataframe_to_csv(
            df=train_df,
            file_path=os.path.join(directory, f"train_df_{self.__get_now()}.csv"),
        )
        save_dataframe_to_csv(
            df=test_df,
            file_path=os.path.join(directory, f"test_df_{self.__get_now()}.csv"),
        )

        x_train = train_df.drop(["date", "store", "item", "sales"], axis=1)
        y_train = train_df.sales

        x_test = test_df.drop(["date", "store", "item", "sales"], axis=1)
        y_test = test_df.sales

        self.__make_model(
            directory=directory,
            model_params=model_params,
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
        )
        logp1_predictions = self.model.predict(x_test=x_test)

        sales = self.preprocess_pipeline.inverse_transform_target(y=y_test)
        predictions = self.preprocess_pipeline.inverse_transform_target(y=logp1_predictions)

        _stores = test_df.store
        if self.stores is not None:
            _stores = _stores[_stores.isin(self.stores)]

        _items = test_df.item
        if self.items is not None:
            _items = _items[_items.isin(self.items)]

        evaluator = Evaluator(
            dates=test_df.date,
            stores=_stores,
            items=_items,
            true_sales=sales,
            predicted_sales=predictions,
            absolute=False,
        )
        evaluator.save_date_based_results(
            file_path=os.path.join(directory, f"{self.model.name}_date_based_results_{self.__get_now()}.csv")
        )
        evaluator.save_week_based_results(
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

        self.__make_model(
            directory=directory,
            model_params=model_params,
            x_train=x_train,
            y_train=y_train,
            x_test=None,
            y_test=None,
        )
        self.onnx_file_path = os.path.join(directory, f"{self.model.name}_{self.__get_now()}.onnx")
        self.model.save_as_onnx(file_path=self.onnx_file_path)

        logger.info("done train...")
