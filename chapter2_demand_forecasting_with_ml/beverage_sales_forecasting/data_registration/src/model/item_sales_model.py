from datetime import date, datetime
from typing import Optional

from pydantic import Extra
from src.model.abstract_model import AbstractModel


class ItemSales(AbstractModel):
    id: str
    date: date
    day_of_week: str
    week_of_year: int
    store_id: str
    item_id: str
    sales: int
    total_sales_amount: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        extra = Extra.forbid
