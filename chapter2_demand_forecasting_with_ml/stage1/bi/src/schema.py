from datetime import date

from pydantic import BaseModel, Extra


class Region(BaseModel):
    id: str
    name: str

    class Config:
        extra = Extra.forbid


class Store(BaseModel):
    id: str
    name: str
    region: str

    class Config:
        extra = Extra.forbid


class Item(BaseModel):
    id: str
    name: str

    class Config:
        extra = Extra.forbid


class ItemSales(BaseModel):
    id: str
    date: date
    day_of_week: str
    week_of_year: int
    store: str
    region: str
    item: str
    item_price: int
    sales: int
    total_sales_amount: int

    class Config:
        extra = Extra.forbid


class ItemWeeklySalesPredictions(BaseModel):
    id: str
    store: str
    region: str
    item: str
    year: int
    week_of_year: int
    prediction: float
    predicted_at: date
    version: int

    class Config:
        extra = Extra.forbid


class ItemWeeklySales(BaseModel):
    id: str
    store: str
    region: str
    item: str
    year: int
    week_of_year: int
    item_price: int
    sales: int
    total_sales_amount: int

    class Config:
        extra = Extra.forbid


class YearWeek(BaseModel):
    year: int
    week_of_year: int
