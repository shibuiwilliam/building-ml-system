from datetime import datetime
from typing import List, Optional

import pandas as pd
from pandera import Check, Column, DataFrameSchema, Index
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


DAYS_OF_WEEK = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

STORES = [
    "nagoya",
    "shinjuku",
    "osaka",
    "kobe",
    "sendai",
    "chiba",
    "morioka",
    "ginza",
    "yokohama",
    "ueno",
]

ITEMS = [
    "fruit_juice",
    "apple_juice",
    "orange_juice",
    "sports_drink",
    "coffee",
    "milk",
    "mineral_water",
    "sparkling_water",
    "soy_milk",
    "beer",
]

_BASE_SCHEMA = {
    "date": Column(datetime),
    "day_of_week": Column(str, checks=Check.isin(DAYS_OF_WEEK)),
    "store": Column(str, checks=Check.isin(STORES)),
    "item": Column(str, checks=Check.isin(ITEMS)),
    "item_price": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "sales": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "total_sales": Column(int, checks=Check.greater_than_or_equal_to(0)),
}

BASE_SCHEMA = DataFrameSchema(
    _BASE_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_PREDICTION_SCHEMA = {
    "date": Column(datetime),
    "day_of_week": Column(str, checks=Check.isin(DAYS_OF_WEEK)),
    "store": Column(str, checks=Check.isin(STORES)),
    "item": Column(str, checks=Check.isin(ITEMS)),
    "item_price": Column(int, checks=Check.greater_than_or_equal_to(0)),
}

PREDICTION_SCHEMA = DataFrameSchema(
    _PREDICTION_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_UPDATED_BASE_SCHEMA = {
    "day_of_month": Column(int, checks=Check(lambda x: x >= 1 and x <= 31, element_wise=True)),
    "day_of_year": Column(int, checks=Check(lambda x: x >= 1 and x <= 366, element_wise=True)),
    "month": Column(int, checks=Check(lambda x: x >= 1 and x <= 12, element_wise=True)),
    "year": Column(int, checks=Check(lambda x: x >= 2000 and x <= 2030, element_wise=True)),
    "week_of_year": Column(int, checks=Check(lambda x: x >= 1 and x <= 53, element_wise=True)),
    "is_month_start": Column(int, checks=Check.isin((0, 1))),
    "is_month_end": Column(int, checks=Check.isin((0, 1))),
}
_UPDATED_SCHEMA = {**_BASE_SCHEMA, **_UPDATED_BASE_SCHEMA}

UPDATED_SCHEMA = DataFrameSchema(
    _UPDATED_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_UPDATED_PREDICTION_SCHEMA = {**_PREDICTION_SCHEMA, **_UPDATED_BASE_SCHEMA}

UPDATED_PREDICTION_SCHEMA = DataFrameSchema(
    _UPDATED_PREDICTION_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)


def load_csv_as_df(
    file_path: str,
    schema: DataFrameSchema = BASE_SCHEMA,
) -> pd.DataFrame:
    logger.info(f"load data from {file_path}")
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    df = schema.validate(df)
    logger.info("done load data")
    return df


def select_by_store_and_item(
    df: pd.DataFrame,
    stores: Optional[List[str]] = None,
    items: Optional[List[str]] = None,
) -> pd.DataFrame:
    if stores is not None:
        logger.info(f"stores to be used: {stores}")
        df = df[df["store"].isin(stores)]
    if items is not None:
        logger.info(f"items to be used: {items}")
        df = df[df["item"].isin(items)]
    return df


def select_and_create_columns(
    df: pd.DataFrame,
    schema: DataFrameSchema = UPDATED_SCHEMA,
) -> pd.DataFrame:
    logger.info("convert data...")
    df["day_of_month"] = df.date.dt.day
    df["day_of_year"] = df.date.dt.dayofyear
    df["month"] = df.date.dt.month
    df["year"] = df.date.dt.year
    df["week_of_year"] = df.date.dt.weekofyear
    df["is_month_start"] = (df.date.dt.is_month_start).astype(int)
    df["is_month_end"] = (df.date.dt.is_month_end).astype(int)
    df.sort_values(by=["store", "item", "date"], axis=0, inplace=True)
    df = df.reset_index(drop=True)
    df = schema.validate(df)
    logger.info("done converting data...")
    return df


def save_dataframe_to_csv(
    df: pd.DataFrame,
    file_path: str,
):
    logger.info(f"save dataframe to {file_path}")
    df.to_csv(file_path, index=False)
