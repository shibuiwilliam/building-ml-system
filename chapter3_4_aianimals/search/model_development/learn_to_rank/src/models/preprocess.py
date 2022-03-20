import os
import sys
from typing import List, Optional, Union

import cloudpickle
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)

cloudpickle.register_pickle_by_value(sys.modules[__name__])


class NumericalMinMaxScaler(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.define_pipeline()

    def define_pipeline(self):
        logger.info("init pipeline")
        self.pipeline = Pipeline(
            [
                (
                    "simple_imputer",
                    SimpleImputer(
                        missing_values=np.nan,
                        strategy="constant",
                        fill_value=0,
                    ),
                ),
                (
                    "min_max_scaler",
                    MinMaxScaler(),
                ),
            ]
        )

        logger.info(f"pipeline: {self.pipeline}")

    def transform(
        self,
        x: List[List[int]],
    ):
        return self.pipeline.transform(x)

    def fit(
        self,
        x: List[List[int]],
        y=None,
    ):
        return self.pipeline.fit(x)

    def fit_transform(
        self,
        x: List[List[int]],
        y=None,
    ):
        return self.pipeline.fit_transform(x)

    def save(
        self,
        file_path: str,
    ) -> str:
        file, ext = os.path.splitext(file_path)
        if ext != ".pkl":
            file_path = f"{file}.pkl"
        logger.info(f"save pipeline: {file_path}")
        with open(file_path, "wb") as f:
            cloudpickle.dump(self, f)
        return file_path


class CategoricalVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.define_pipeline()

    def define_pipeline(self):
        logger.info("init pipeline")
        self.pipeline = Pipeline(
            [
                (
                    "simple_imputer",
                    SimpleImputer(
                        missing_values=np.nan,
                        strategy="constant",
                        fill_value=None,
                    ),
                ),
                (
                    "one_hot_encoder",
                    OneHotEncoder(
                        sparse=True,
                        handle_unknown="ignore",
                    ),
                ),
            ]
        )

        logger.info(f"pipeline: {self.pipeline}")

    def transform(
        self,
        x: List[List[Optional[Union[int, str]]]],
    ):
        return self.pipeline.transform(x)

    def fit(
        self,
        x: List[List[Optional[Union[int, str]]]],
        y=None,
    ):
        return self.pipeline.fit(x)

    def fit_transform(
        self,
        x: List[List[Optional[Union[int, str]]]],
        y=None,
    ):
        return self.pipeline.fit_transform(x)

    def save(
        self,
        file_path: str,
    ) -> str:
        file, ext = os.path.splitext(file_path)
        if ext != ".pkl":
            file_path = f"{file}.pkl"
        logger.info(f"save pipeline: {file_path}")
        with open(file_path, "wb") as f:
            cloudpickle.dump(self, f)
        return file_path
