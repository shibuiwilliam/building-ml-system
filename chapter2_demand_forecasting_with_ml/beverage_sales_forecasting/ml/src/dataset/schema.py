from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum

import pandas as pd
from pandera import Check, Column, DataFrameSchema, Index
from pydantic import BaseModel, Extra
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


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

WEEKS = [i for i in range(1, 54, 1)]

MONTHS = [i for i in range(1, 13, 1)]

YEARS = [i for i in range(2017, 2031, 1)]

DAYS_OF_WEEK = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

_BASE_SCHEMA = {
    "date": Column(datetime),
    "year": Column(int, required=False),
    "day_of_week": Column(str, checks=Check.isin(DAYS_OF_WEEK)),
    "week_of_year": Column(int, checks=Check.isin(WEEKS)),
    "store": Column(str, checks=Check.isin(STORES)),
    "item": Column(str, checks=Check.isin(ITEMS)),
    "item_price": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "sales": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "total_sales_amount": Column(int, checks=Check.greater_than_or_equal_to(0)),
}
BASE_SCHEMA = DataFrameSchema(
    _BASE_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_WEEKLY_SCHEMA = {
    "year": Column(int),
    "week_of_year": Column(int, checks=Check.isin(WEEKS)),
    "month": Column(int, checks=Check.isin(MONTHS)),
    "store": Column(str, checks=Check.isin(STORES)),
    "item": Column(str, checks=Check.isin(ITEMS)),
    "item_price": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "sales": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "total_sales_amount": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "sales_lag_.*": Column(float, checks=Check.greater_than_or_equal_to(0), nullable=True, regex=True),
}
WEEKLY_SCHEMA = DataFrameSchema(
    _WEEKLY_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_PREPROCESSED_SCHEMA = {
    "store": Column(str, checks=Check.isin(STORES)),
    "item": Column(str, checks=Check.isin(ITEMS)),
    "year": Column(int, checks=Check.isin(YEARS)),
    "week_of_year": Column(int, checks=Check.isin(WEEKS)),
    "sales.*": Column(
        float,
        checks=Check(lambda x: x >= 0.0 and x <= 5000.0, element_wise=True),
        nullable=True,
        regex=True,
    ),
    "item_price": Column(float, checks=Check(lambda x: x >= 0.0 and x <= 1.0, element_wise=True)),
    "store_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
    "item_.*[^price]": Column(float, checks=Check.isin((0, 1)), regex=True),
    "week_of_year_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
    "month_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
    "year_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
}
PREPROCESSED_SCHEMA = DataFrameSchema(
    _PREPROCESSED_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_X_SCHEMA = {
    "year": Column(int, checks=Check.isin(YEARS)),
    "week_of_year": Column(int, checks=Check.isin(WEEKS)),
    "sales_.*": Column(
        float,
        checks=Check(lambda x: x >= 0.0 and x <= 5000.0, element_wise=True),
        nullable=True,
        regex=True,
    ),
    "item_price": Column(float, checks=Check(lambda x: x >= 0.0 and x <= 1.0, element_wise=True)),
    "store_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
    "item_.*[^price]": Column(float, checks=Check.isin((0, 1)), regex=True),
    "week_of_year_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
    "month_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
    "year_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
}
X_SCHEMA = DataFrameSchema(
    _X_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_Y_SCHEMA = {
    "sales": Column(
        float,
        checks=Check(lambda x: x >= 0.0 and x <= 5000.0, element_wise=True),
    )
}
Y_SCHEMA = DataFrameSchema(
    _Y_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)

_WEEKLY_PREDICTION_SCHEMA = {
    "year": Column(int),
    "week_of_year": Column(int, checks=Check.isin(WEEKS)),
    "store": Column(str, checks=Check.isin(STORES)),
    "item": Column(str, checks=Check.isin(ITEMS)),
    "item_price": Column(int, checks=Check.greater_than_or_equal_to(0)),
    "prediction": Column(float, checks=Check.greater_than_or_equal_to(0)),
}
WEEKLY_PREDICTION_SCHEMA = DataFrameSchema(
    _WEEKLY_PREDICTION_SCHEMA,
    index=Index(int),
    strict=True,
    coerce=True,
)


class YearAndWeek(BaseModel):
    year: int
    week_of_year: int

    class Config:
        extra = Extra.forbid


class TABLES(Enum):
    REGIONS = "regions"
    STORES = "stores"
    ITEMS = "items"
    ITEM_PRICES = "item_prices"
    ITEM_SALES_RECORDS = "item_sales"
    ITEM_WEEKLY_SALES_PREDICTIONS = "item_weekly_sales_predictions"


class ItemSales(BaseModel):
    date: date
    day_of_week: str
    week_of_year: int
    store: str
    item: str
    item_price: int
    sales: int
    total_sales_amount: int

    class Config:
        extra = Extra.forbid


class ItemWeeklySalesPredictions(BaseModel):
    store: str
    item: str
    year: int
    week_of_year: int
    prediction: float
    predicted_at: date

    class Config:
        extra = Extra.forbid


@dataclass
class XY:
    x: pd.DataFrame
    y: pd.DataFrame
