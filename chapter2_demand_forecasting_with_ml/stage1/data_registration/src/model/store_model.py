from datetime import datetime
from typing import Optional

from pydantic import Extra
from src.model.abstract_model import AbstractModel


class Store(AbstractModel):
    id: str
    name: str
    region_id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        extra = Extra.forbid
