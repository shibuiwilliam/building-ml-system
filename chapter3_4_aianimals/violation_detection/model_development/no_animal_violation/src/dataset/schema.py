from typing import List

from pydantic import BaseModel


class ImageShape(BaseModel):
    height: int = 224
    width: int = 224
    depth: int = 3
    color: str = "RGB"


class Dataset(BaseModel):
    negative_filepaths: List[str]
    positive_filepaths: List[str]


class TrainTestDataset(BaseModel):
    train_dataset: Dataset
    test_dataset: Dataset
