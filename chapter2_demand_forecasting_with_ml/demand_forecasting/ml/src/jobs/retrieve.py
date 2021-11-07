from datetime import datetime
from typing import Tuple

import pandas as pd
from omegaconf import DictConfig
from src.dataset.data_manager import DATA_SOURCE, DBDataManager, load_df_from_csv
from src.dataset.schema import BASE_SCHEMA, X_SCHEMA, XY, Y_SCHEMA, YearAndWeek
from src.middleware.db_client import DBClient
from src.middleware.logger import configure_logger
from src.models.preprocess import DataPreprocessPipeline

logger = configure_logger(__name__)


class DataRetriever(object):
    def __init__(self):
        pass

    def retrieve_dataset(
        self,
        cfg: DictConfig,
        data_source: DATA_SOURCE = DATA_SOURCE.LOCAL,
    ) -> pd.DataFrame:
        logger.info("start retrieve data")
        if data_source == DATA_SOURCE.LOCAL:
            raw_df = load_df_from_csv(file_path=cfg.jobs.data.path)
        elif data_source == DATA_SOURCE.DB:
            db_client = DBClient()
            db_data_manager = DBDataManager(db_client=db_client)

            date_from = cfg.jobs.data.target_data.get("date_from", None)
            if date_from is not None:
                date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
            date_to = cfg.jobs.data.target_data.get("date_to", None)
            if date_to is not None:
                date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
            item = cfg.jobs.data.target_data.get("item", None)
            if item == "ALL":
                item = None
            store = cfg.jobs.data.target_data.get("store", None)
            if store == "ALL":
                store = None
            region = cfg.jobs.data.target_data.get("region", None)
            if region == "ALL":
                region = None

            raw_df = db_data_manager.load_df_from_db(
                date_from=date_from,
                date_to=date_to,
                item=item,
                store=store,
                region=region,
            )
        else:
            raise ValueError

        raw_df["date"] = pd.to_datetime(raw_df["date"])
        raw_df = BASE_SCHEMA.validate(raw_df)
        logger.info(
            f"""
raw_df columns: {raw_df.columns}
raw_df shape: {raw_df.shape}
    """
        )
        return raw_df

    def train_test_split(
        self,
        raw_df: pd.DataFrame,
        train_year_and_week: YearAndWeek,
        test_year_and_week: YearAndWeek,
        data_preprocess_pipeline: DataPreprocessPipeline,
    ) -> Tuple[XY, XY]:
        logger.info(
            f"""
train from {train_year_and_week.year} of {train_year_and_week.week_of_year} to {test_year_and_week.year} {test_year_and_week.week_of_year-2}
test from {test_year_and_week.year} {test_year_and_week.week_of_year}
                """
        )

        weekly_df = data_preprocess_pipeline.preprocess(x=raw_df)

        weekly_train_df = weekly_df[
            (weekly_df.year == train_year_and_week.year) & (weekly_df.week_of_year >= train_year_and_week.week_of_year)
            | ((weekly_df.year > train_year_and_week.year) & (weekly_df.year < test_year_and_week.year))
            | (
                (weekly_df.year == test_year_and_week.year)
                & (weekly_df.week_of_year <= test_year_and_week.week_of_year - 2)
            )
        ].reset_index(drop=True)

        weekly_test_df = weekly_df[
            (weekly_df.year == test_year_and_week.year) & (weekly_df.week_of_year >= test_year_and_week.week_of_year)
            | (weekly_df.year > test_year_and_week.year)
        ].reset_index(drop=True)
        logger.info(
            f"""
weekly train df columns: {weekly_train_df.columns}
weekly train df shape: {weekly_train_df.shape}
weekly test df columns: {weekly_test_df.columns}
weekly test df shape: {weekly_test_df.shape}
    """
        )

        preprocessed_train_df = data_preprocess_pipeline.fit_transform(x=weekly_train_df)
        preprocessed_test_df = data_preprocess_pipeline.transform(x=weekly_test_df)
        logger.info(
            f"""
preprocessed train df columns: {preprocessed_train_df.columns}
preprocessed train df shape: {preprocessed_train_df.shape}
preprocessed test df columns: {preprocessed_test_df.columns}
preprocessed test df shape: {preprocessed_test_df.shape}
    """
        )

        x_train = (
            preprocessed_train_df[data_preprocess_pipeline.preprocessed_columns]
            .drop(["sales", "store", "item"], axis=1)
            .reset_index(drop=True)
        )
        y_train = preprocessed_train_df[["sales"]].reset_index(drop=True)
        x_test = (
            preprocessed_test_df[data_preprocess_pipeline.preprocessed_columns]
            .drop(["sales", "store", "item"], axis=1)
            .reset_index(drop=True)
        )
        y_test = preprocessed_test_df[["sales"]].reset_index(drop=True)

        x_train = X_SCHEMA.validate(x_train)
        y_train = Y_SCHEMA.validate(y_train)
        x_test = X_SCHEMA.validate(x_test)
        y_test = Y_SCHEMA.validate(y_test)

        logger.info(
            f"""
x_train shape: {x_train.shape}
y_train shape: {y_train.shape}
x_test shape: {x_test.shape}
y_test shape: {y_test.shape}
    """
        )

        logger.info("done retrieve data")
        return XY(x=x_train, y=y_train), XY(x=x_test, y=y_test)
