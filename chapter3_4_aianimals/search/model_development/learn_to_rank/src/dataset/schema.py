from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
from pydantic import BaseModel, Extra


class Action(Enum):
    SELECT = "select"
    SEE_LONG = "see_long"
    LIKE = "like"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in Action.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in Action.__members__.values()]

    @staticmethod
    def value_to_key(value: Optional[str] = None) -> Optional[Enum]:
        if value is None:
            return None
        for v in [v for v in Action.__members__.values()]:
            if value == v.value:
                return v
        return None


class TABLES(Enum):
    ANIMAL = "animals"
    ACCESS_LOG = "access_logs"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in TABLES.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in TABLES.__members__.values()]


class Animal(BaseModel):
    id: str
    animal_category_id: int
    animal_subcategory_id: int
    user_id: str
    name: str
    description: str
    photo_url: str
    deactivated: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class AccessLogBase(BaseModel):
    id: str
    query_phrases: List[str]
    query_animal_category_id: Optional[int] = None
    query_animal_subcategory_id: Optional[int] = None
    user_id: str
    likes: int
    action: str
    animal_id: str


class AccessLog(AccessLogBase):
    animal_category_id: int
    animal_subcategory_id: int
    name: str
    description: str

    class Config:
        extra = Extra.forbid


class AnimalFeature(BaseModel):
    id: str
    name_words: Union[Dict, List]
    name_vector: Union[Dict, List]
    description_words: Union[Dict, List]
    description_vector: Union[Dict, List]
    created_at: datetime
    updated_at: datetime


class RawData(BaseModel):
    data: List[Dict]
    target: List[List[int]]


@dataclass
class SplitData(object):
    x_train: pd.DataFrame
    x_test: pd.DataFrame
    y_train: np.ndarray
    y_test: np.ndarray
    q_train: Optional[List[int]]
    q_test: Optional[List[int]]
