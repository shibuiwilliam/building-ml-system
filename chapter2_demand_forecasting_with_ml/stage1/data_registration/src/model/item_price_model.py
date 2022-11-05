from datetime import date, datetime
from typing import Optional

from pydantic import Extra
from src.model.abstract_model import AbstractModel


class ItemPrice(AbstractModel):
    id: str
    item_id: str
    price: int
    applied_from: date
    applied_to: date
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        extra = Extra.forbid


class ItemPriceUpdate(AbstractModel):
    id: str
    price: Optional[int]
    applied_from: Optional[date]
    applied_to: Optional[date]

    class Config:
        extra = Extra.forbid
