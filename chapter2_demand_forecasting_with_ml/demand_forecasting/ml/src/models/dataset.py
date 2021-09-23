from datetime import date, datetime
from typing import Tuple

import pandas as pd
from pandera import Check, Column, DataFrameSchema, Index

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

_UPDATED_SCHEMA = {c: s for c, s in _BASE_SCHEMA.items()}
_UPDATED_SCHEMA["day_of_month"] = Column(int, checks=Check(lambda x: x >= 1 and x <= 31, element_wise=True))
_UPDATED_SCHEMA["day_of_year"] = Column(int, checks=Check(lambda x: x >= 1 and x <= 366, element_wise=True))
_UPDATED_SCHEMA["month"] = Column(int, checks=Check(lambda x: x >= 1 and x <= 12, element_wise=True))
_UPDATED_SCHEMA["year"] = Column(int, checks=Check(lambda x: x >= 2000 and x <= 2030, element_wise=True))
_UPDATED_SCHEMA["week_of_year"] = Column(int, checks=Check(lambda x: x >= 1 and x <= 53, element_wise=True))
_UPDATED_SCHEMA["is_month_start"] = Column(int, checks=Check.isin((0, 1)))
_UPDATED_SCHEMA["is_month_end"] = Column(int, checks=Check.isin((0, 1)))

UPDATED_SCHEMA = DataFrameSchema(
    _UPDATED_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)


def load_csv_as_df(
    file_path: str,
    schema: DataFrameSchema = BASE_SCHEMA,
) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    df = schema.validate(df)
    return df


def select_and_create_columns(
    df: pd.DataFrame,
    schema: DataFrameSchema = UPDATED_SCHEMA,
) -> pd.DataFrame:
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
    return df


def train_test_split_by_date(
    df_data: pd.DataFrame,
    train_start_date: date,
    train_end_date: date,
    test_start_date: date,
    test_end_date: date,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_train = df_data[df_data["date"] >= train_start_date][df_data["date"] <= train_end_date].reset_index(drop=True)
    df_test = df_data[df_data["date"] >= test_start_date][df_data["date"] <= test_end_date].reset_index(drop=True)
    return df_train, df_test
