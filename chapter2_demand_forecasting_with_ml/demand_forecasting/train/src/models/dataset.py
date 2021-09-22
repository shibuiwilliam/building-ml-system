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

SCHEMA = DataFrameSchema(
    {
        "date": Column(datetime),
        "day_of_week": Column(str, checks=Check.isin(DAYS_OF_WEEK)),
        "store": Column(str, checks=Check.isin(STORES)),
        "item": Column(str, checks=Check.isin(ITEMS)),
        "item_price": Column(int, checks=Check.greater_than_or_equal_to(0)),
        "sales": Column(int, checks=Check.greater_than_or_equal_to(0)),
        "total_sales": Column(int, checks=Check.greater_than_or_equal_to(0)),
    },
    index=Index(int),
    strict=True,
    coerce=True,
)


def load_csv_as_df(
    file_path: str,
    schema: DataFrameSchema = SCHEMA,
) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    df = schema.validate(df)
    return df


def select_and_create_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_data = df.drop(["sales", "total_sales"], axis=True)
    df_data["day_of_month"] = df_data.date.dt.day
    df_data["day_of_year"] = df_data.date.dt.dayofyear
    df_data["month"] = df_data.date.dt.month
    df_data["year"] = df_data.date.dt.year
    df_data["week_of_year"] = df_data.date.dt.weekofyear
    df_data["is_month_start"] = (df_data.date.dt.is_month_start).astype(int)
    df_data["is_month_end"] = (df_data.date.dt.is_month_end).astype(int)
    df_data.sort_values(by=["store", "item", "date"], axis=0, inplace=True)
    df_data = df_data.reset_index(drop=True)

    df_label = df[["date", "store", "item", "sales"]]
    df_label.sort_values(by=["store", "item", "date"], axis=0, inplace=True)
    return df_data, df_label


def train_test_split_by_date(
    df_data: pd.DataFrame,
    df_label: pd.DataFrame,
    boundary_date: date,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    x_train = df_data[df_data["date"] <= boundary_date].reset_index(drop=True)
    x_test = df_data[df_data["date"] > boundary_date].reset_index(drop=True)
    y_train = df_label[df_label["date"] <= boundary_date].reset_index(drop=True)
    y_test = df_label[df_label["date"] > boundary_date].reset_index(drop=True)
    return x_train, x_test, y_train, y_test
