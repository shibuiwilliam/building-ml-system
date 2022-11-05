from datetime import date, datetime

import pandas as pd
from pandera import Check, Column, DataFrameSchema, Index
from pydantic import BaseModel, Extra

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

ITEM_PRICES = {
    "fruit_juice": 150,
    "apple_juice": 120,
    "orange_juice": 120,
    "sports_drink": 130,
    "coffee": 200,
    "milk": 130,
    "mineral_water": 100,
    "sparkling_water": 120,
    "soy_milk": 120,
    "beer": 200,
}

WEEKS = [i for i in range(1, 54, 1)]

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


class Store(BaseModel):
    name: str

    class Config:
        extra = Extra.forbid


class Item(BaseModel):
    name: str

    class Config:
        extra = Extra.forbid
