from datetime import date
from typing import Optional, Tuple

import pandas as pd
from src.dataset.data_manager import DBDataManager
from src.dataset.schema import BASE_SCHEMA, RAW_PREDICTION_SCHEMA, X_SCHEMA, XY, Y_SCHEMA, YearAndWeek
from src.middleware.logger import configure_logger
from src.models.preprocess import DataPreprocessPipeline

logger = configure_logger(__name__)


class DataRetriever(object):
    def __init__(
        self,
        db_data_manager: DBDataManager,
    ):
        self.db_data_manager = db_data_manager

    def retrieve_item_sales_earliest_date(self) -> Optional[date]:
        data = self.db_data_manager.select_earliest_day_item_sales()
        if len(data) == 0:
            return None
        return data[0].date

    def retrieve_item_sales_latest_date(self) -> Optional[date]:
        data = self.db_data_manager.select_latest_day_item_sales()
        if len(data) == 0:
            return None
        return data[0].date

    def retrieve_dataset(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        item: str = "ALL",
        store: str = "ALL",
        region: str = "ALL",
    ) -> pd.DataFrame:
        logger.info("start retrieve data")

        if item == "ALL":
            item = None
        if store == "ALL":
            store = None
        if region == "ALL":
            region = None

        raw_df = self.db_data_manager.load_df_from_db(
            date_from=date_from,
            date_to=date_to,
            item=item,
            store=store,
            region=region,
        )

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
        train_end_year_and_week: YearAndWeek,
        test_year_and_week: YearAndWeek,
        data_preprocess_pipeline: DataPreprocessPipeline,
    ) -> Tuple[XY, XY]:
        logger.info(
            f"""
train: {train_year_and_week.year} {train_year_and_week.week_of_year} to {train_end_year_and_week.year} {train_end_year_and_week.week_of_year}
test: {test_year_and_week.year} {test_year_and_week.week_of_year}
                """
        )

        weekly_df = data_preprocess_pipeline.preprocess(x=raw_df)

        weekly_train_df = weekly_df[
            (weekly_df.year == train_year_and_week.year) & (weekly_df.week_of_year >= train_year_and_week.week_of_year)
            | ((weekly_df.year > train_year_and_week.year) & (weekly_df.year < test_year_and_week.year))
            | (
                (weekly_df.year == train_end_year_and_week.year)
                & (weekly_df.week_of_year <= train_end_year_and_week.week_of_year)
            )
        ].reset_index(drop=True)

        weekly_test_df = weekly_df[
            (weekly_df.year == test_year_and_week.year) & (weekly_df.week_of_year == test_year_and_week.week_of_year)
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

    def retrieve_prediction_latest_date(self) -> Optional[date]:
        data = self.db_data_manager.select_latest_prediction()
        if len(data) == 0:
            return None
        return date.fromisocalendar(
            year=data[0].year,
            week=data[0].week_of_year,
            day=7,
        )

    def retrieve_prediction_data(
        self,
        date_from: date,
        date_to: date,
    ) -> pd.DataFrame:
        logger.info("start retrieve data")

        data_to_be_predicted = self.db_data_manager.select_prediction_data(
            date_from=date_from,
            date_to=date_to,
        )
        data_to_be_predicted_df = pd.DataFrame([d.dict() for d in data_to_be_predicted])
        data_to_be_predicted_df["date"] = pd.to_datetime(data_to_be_predicted_df["date"])
        data_to_be_predicted_df = RAW_PREDICTION_SCHEMA.validate(data_to_be_predicted_df)

        logger.info(
            f"""
data_to_be_predicted columns: {data_to_be_predicted_df.columns}
data_to_be_predicted shape: {data_to_be_predicted_df.shape}
    """
        )
        return data_to_be_predicted_df
