from dataclasses import dataclass
from enum import Enum
from typing import List

import numpy as np
from pydantic import BaseModel, Extra


class TABLES(Enum):
    ANIMAL = "animals"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in TABLES.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in TABLES.__members__.values()]


class Animal(BaseModel):
    id: str
    photo_url: str
    deactivated: bool = False

    class Config:
        extra = Extra.forbid


class DownloadedImage(BaseModel):
    id: str
    path: str


class DownloadedImages(BaseModel):
    images: List[DownloadedImage]


@dataclass
class Dataset(object):
    data: np.ndarray
    ids: List[str]
