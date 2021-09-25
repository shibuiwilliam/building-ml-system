from datetime import date, datetime
from typing import Optional

from pandera import Check, Column, DataFrameSchema, Index
from pydantic import BaseModel
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


class ItemSale(BaseModel):
    id: str
    item_id: str
    store_id: str
    item_price_id: str
    quantity: int
    total_sales: int
    sold_at: date
    day_of_week: str
    item_name: str
    store_name: str
    price: int
    created_at: datetime
    updated_at: datetime


class ItemPrice(BaseModel):
    id: str
    item_id: str
    price: int
    applied_from: date
    applied_to: Optional[date]
    item_name: str
    created_at: datetime
    updated_at: datetime


class PredictionTarget(BaseModel):
    store_name: str
    item_name: str
    date: date
    day_of_week: str
    price: int
