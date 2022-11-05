from datetime import date
from typing import List, Optional, Tuple

import pandas as pd
from src.dataset.data_manager import load_df_from_csv
from src.dataset.schema import (
    BASE_SCHEMA,
    DAYS_OF_WEEK,
    ITEM_PRICES,
    ITEMS,
    STORES,
    X_SCHEMA,
    XY,
    Y_SCHEMA,
    DataToBePredicted,
    YearAndWeek,
)
from src.middleware.dates import dates_in_between_dates
from src.middleware.logger import configure_logger
from src.models.preprocess import DataPreprocessPipeline

logger = configure_logger(__name__)


class DataRetriever(object):
    def __init__(self):
        pass

    def retrieve_dataset(
        self,
        file_path: str,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        item: str = "ALL",
        store: str = "ALL",
    ) -> pd.DataFrame:
        logger.info("start retrieve data")
        raw_df = load_df_from_csv(file_path=file_path)
        raw_df["date"] = pd.to_datetime(raw_df["date"]).dt.date
        if date_from is not None:
            raw_df = raw_df[raw_df.date >= date_from]
        if date_to is not None:
            raw_df = raw_df[raw_df.date <= date_to]
        if item is not None and item != "ALL":
            raw_df = raw_df[raw_df.item == item]
        if store is not None and store != "ALL":
            raw_df = raw_df[raw_df.store == store]

        raw_df = BASE_SCHEMA.validate(raw_df)
        logger.info(
            f"""
Loaded dataset
raw_df columns: {raw_df.columns}
raw_df shape: {raw_df.shape}
date from: {raw_df.date.min()}
date to: {raw_df.date.max()}
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
Split dataset
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

        logger.info("done split data")
        return XY(x=x_train, y=y_train), XY(x=x_test, y=y_test)

    def retrieve_prediction_data(
        self,
        date_from: date,
        date_to: date,
    ) -> pd.DataFrame:
        logger.info("start retrieve prediction data")
        data: List[DataToBePredicted] = []
        dates = dates_in_between_dates(
            date_from=date_from,
            date_to=date_to,
        )
        for d in dates:
            for s in STORES:
                for i in ITEMS:
                    isocalendar = d.isocalendar()
                    data.append(
                        DataToBePredicted(
                            date=d,
                            day_of_week=DAYS_OF_WEEK[isocalendar.weekday - 1],
                            week_of_year=isocalendar.week,
                            store=s,
                            item=i,
                            item_price=ITEM_PRICES[i],
                            sales=0,
                            total_sales_amount=0,
                        ),
                    )
        data_to_be_predicted_df = pd.DataFrame([d.dict() for d in data])
        logger.info(
            f"""
Loaded prediction dataset
columns: {data_to_be_predicted_df.columns}
shape: {data_to_be_predicted_df.shape}
date from: {data_to_be_predicted_df.date.min()}
date to: {data_to_be_predicted_df.date.max()}
    """
        )
        return data_to_be_predicted_df
