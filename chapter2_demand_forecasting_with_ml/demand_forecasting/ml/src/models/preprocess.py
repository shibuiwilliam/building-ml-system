from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Any, Dict, List, Tuple, Union

import numpy as np
import pandas as pd
from joblib import dump, load
from pandera import Check, Column, DataFrameSchema, Index
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler, OneHotEncoder
from src.models.dataset import DAYS_OF_WEEK, ITEMS, STORES
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


class ItemSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        if self.key in x.columns:
            return x[[self.key]]
        return None


class ItemsSelector(BaseEstimator, TransformerMixin):
    def __init__(self, keys):
        self.keys = keys

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        existing_keys = []
        for key in self.keys:
            if key in x.columns:
                existing_keys.append(key)
        if len(existing_keys) == 0:
            return None
        return x[self.keys]


class Log1pTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        if x is not None:
            return np.log1p(x)
        return None


class Expm1Transformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return np.expm1(x)


class BasePreprocessPipeline(ABC, BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    @abstractmethod
    def fit(
        self,
        x: pd.DataFrame,
        y=None,
    ):
        raise NotImplementedError

    @abstractmethod
    def transform(
        self,
        x: pd.DataFrame,
    ) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def fit_transform(
        self,
        x: pd.DataFrame,
        y=None,
    ) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def inverse_transform_target(
        self,
        y: pd.DataFrame,
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def to_dataframe(
        self,
        base_dataframe: pd.DataFrame,
        x: np.ndarray,
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def train_test_split_by_date(
        self,
        preprocessed_df: pd.DataFrame,
        train_start_date: date,
        train_end_date: date,
        test_start_date: date,
        test_end_date: date,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        raise NotImplementedError

    @abstractmethod
    def dump_pipeline(self, file_path: str):
        raise NotImplementedError

    @abstractmethod
    def load_pipeline(self, file_path: str):
        raise NotImplementedError


class DataPreprocessPipeline(BasePreprocessPipeline):
    def __init__(
        self,
        include_target: bool = True,
    ):
        self.include_target = include_target

        self.day_of_week = [[d] for d in DAYS_OF_WEEK]
        self.day_of_month = [[i] for i in range(1, 32, 1)]
        self.week_of_year = [[i] for i in range(1, 54, 1)]
        self.months = [[i] for i in range(1, 13, 1)]
        self.years = [[i] for i in range(2017, 2031, 1)]
        self.day_of_week_ohe = OneHotEncoder(sparse=True, handle_unknown="ignore").fit(self.day_of_week)
        self.day_of_month_ohe = OneHotEncoder(sparse=True, handle_unknown="ignore").fit(self.day_of_month)
        self.week_of_year_ohe = OneHotEncoder(sparse=True, handle_unknown="ignore").fit(self.week_of_year)
        self.months_ohe = OneHotEncoder(sparse=True, handle_unknown="ignore").fit(self.months)
        self.years_ohe = OneHotEncoder(sparse=True, handle_unknown="ignore").fit(self.years)
        self.day_of_week_ohe_transformer = FunctionTransformer(self.day_of_week_ohe.transform)
        self.day_of_month_ohe_transformer = FunctionTransformer(self.day_of_month_ohe.transform)
        self.week_of_year_ohe_transformer = FunctionTransformer(self.week_of_year_ohe.transform)
        self.months_ohe_transformer = FunctionTransformer(self.months_ohe.transform)
        self.years_ohe_transformer = FunctionTransformer(self.years_ohe.transform)

        self.constant_pipelines = []
        for name, transformer in zip(
            ("day_of_week", "day_of_month", "week_of_year", "month", "year"),
            (
                self.day_of_week_ohe_transformer,
                self.day_of_month_ohe_transformer,
                self.week_of_year_ohe_transformer,
                self.months_ohe_transformer,
                self.years_ohe_transformer,
            ),
        ):
            pipeline = (
                name,
                Pipeline(
                    [
                        (
                            "selector",
                            ItemsSelector(keys=[name]),
                        ),
                        (
                            "simple_imputer",
                            SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                        ),
                        (
                            "one_hot_encoder",
                            transformer,
                        ),
                    ]
                ),
            )
            self.constant_pipelines.append(pipeline)

        self.bare_pipeline = (
            "bare_pipeline",
            Pipeline(
                [
                    (
                        "selector",
                        ItemsSelector(
                            keys=[
                                "is_month_start",
                                "is_month_end",
                            ],
                        ),
                    ),
                    (
                        "simple_imputer",
                        SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                    ),
                ]
            ),
        )

        self.numerical_pipeline = (
            "numerical_pipeline",
            Pipeline(
                [
                    (
                        "selector",
                        ItemsSelector(
                            keys=[
                                "item_price",
                                "day_of_year",
                            ],
                        ),
                    ),
                    (
                        "simple_imputer",
                        SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                    ),
                    (
                        "standard_scaler",
                        MinMaxScaler(),
                    ),
                ]
            ),
        )

        self.category_pipeline = (
            "category_pipeline",
            Pipeline(
                [
                    (
                        "selector",
                        ItemsSelector(
                            keys=[
                                "store",
                                "item",
                            ],
                        ),
                    ),
                    (
                        "simple_imputer",
                        SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                    ),
                    (
                        "one_hot_encoder",
                        OneHotEncoder(sparse=True, handle_unknown="ignore"),
                    ),
                ]
            ),
        )

        self.target_pipeline = (
            "target_pipeline",
            Pipeline(
                [
                    (
                        "selector",
                        ItemsSelector(
                            keys=[
                                "sales",
                            ],
                        ),
                    ),
                    (
                        "log1p_transformer",
                        Log1pTransformer(),
                    ),
                ]
            ),
        )

        self.pipeline: FeatureUnion = FeatureUnion(
            [
                self.target_pipeline,
                self.numerical_pipeline,
                self.bare_pipeline,
                self.category_pipeline,
                *self.constant_pipelines,
            ]
        )

        self.preprocessed_columns: List[str] = []
        self.types: Dict[str, str] = {}

        self._schema = {
            "date": Column(datetime),
            "store": Column(str, checks=Check.isin(STORES)),
            "item": Column(str, checks=Check.isin(ITEMS)),
            "item_price": Column(float, checks=Check(lambda x: x >= 0.0 and x <= 1.0, element_wise=True)),
            "day_of_year": Column(float, checks=Check(lambda x: x >= 0.0 and x <= 1.0, element_wise=True)),
            "is_month_start": Column(float, checks=Check.isin((0, 1))),
            "is_month_end": Column(float, checks=Check.isin((0, 1))),
            "store_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
            "item_.*[^price]": Column(float, checks=Check.isin((0, 1)), regex=True),
            "day_of_week_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
            "day_of_month_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
            "week_of_year_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
            "month_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
            "year_.*": Column(float, checks=Check.isin((0, 1)), regex=True),
        }

        if self.include_target:
            self._schema["sales"] = Column(float, checks=Check.greater_than_or_equal_to(0))

        self.schema = DataFrameSchema(
            self._schema,
            index=Index(int),
            strict=True,
            coerce=True,
        )

    def fit(
        self,
        x: Union[np.ndarray, pd.DataFrame, pd.Series],
        y=None,
    ):
        self.pipeline.fit(x)
        return self

    def transform(
        self,
        x: Union[np.ndarray, pd.DataFrame, pd.Series],
    ) -> np.ndarray:
        _x = self.pipeline.transform(x)
        self.__set_columns()
        return _x

    def fit_transform(
        self,
        x: Union[np.ndarray, pd.DataFrame, pd.Series],
        y=None,
    ) -> np.ndarray:
        _x = self.pipeline.fit_transform(x)
        self.__set_columns()
        return _x

    def inverse_transform_target(
        self,
        y: Union[np.ndarray, pd.Series],
    ) -> Union[np.ndarray, pd.Series]:
        return Expm1Transformer().fit_transform(y)

    def __set_columns(self):
        self.preprocessed_columns = []

        store_categories = [
            f"store_{c}" for c in self.pipeline.transformer_list[3][-1].steps[-1][-1].categories_[0].tolist()
        ]
        item_categories = [
            f"item_{c}" for c in self.pipeline.transformer_list[3][-1].steps[-1][-1].categories_[1].tolist()
        ]
        day_of_week_categories = [f"day_of_week_{c}" for c in self.day_of_week_ohe.categories_[0].tolist()]
        day_of_month_categories = [f"day_of_month_{c}" for c in self.day_of_month_ohe.categories_[0].tolist()]
        week_of_year_categories = [f"week_of_year_{c}" for c in self.week_of_year_ohe.categories_[0].tolist()]
        months_categories = [f"month_{c}" for c in self.months_ohe.categories_[0].tolist()]
        years_categories = [f"year_{c}" for c in self.years_ohe.categories_[0].tolist()]
        if self.include_target:
            self.preprocessed_columns.append("sales")
        self.preprocessed_columns.extend(["item_price", "day_of_year", "is_month_start", "is_month_end"])
        self.preprocessed_columns.extend(store_categories)
        self.preprocessed_columns.extend(item_categories)
        self.preprocessed_columns.extend(day_of_week_categories)
        self.preprocessed_columns.extend(day_of_month_categories)
        self.preprocessed_columns.extend(week_of_year_categories)
        self.preprocessed_columns.extend(months_categories)
        self.preprocessed_columns.extend(years_categories)

        self.types = {c: "float64" for c in self.preprocessed_columns}

        logger.debug(f"columns and types: {self.types}")

    def to_dataframe(
        self,
        base_dataframe: pd.DataFrame,
        x: np.ndarray,
    ) -> pd.DataFrame:
        logger.info("convert to dataframe")
        _x = x if isinstance(x, np.ndarray) else x.toarray()
        preprocessed_df = pd.DataFrame(_x, columns=self.preprocessed_columns).astype(self.types)
        preprocessed_df = pd.concat([base_dataframe[["date", "store", "item"]], preprocessed_df], axis=1)
        preprocessed_df = self.schema.validate(preprocessed_df)
        return preprocessed_df

    def train_test_split_by_date(
        self,
        preprocessed_df: pd.DataFrame,
        train_start_date: date,
        train_end_date: date,
        test_start_date: date,
        test_end_date: date,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        logger.info(
            f"train test split by date: from {train_start_date} to {train_end_date} and from {test_start_date} to {test_end_date}"
        )
        train_df = preprocessed_df[preprocessed_df["date"] >= train_start_date][
            preprocessed_df["date"] <= train_end_date
        ].reset_index(drop=True)
        test_df = preprocessed_df[preprocessed_df["date"] >= test_start_date][
            preprocessed_df["date"] <= test_end_date
        ].reset_index(drop=True)
        return train_df, test_df

    def dump_pipeline(self, file_path: str):
        logger.info(f"save preprocess pipeline: {file_path}")
        dump(self.pipeline, file_path)

    def load_pipeline(self, file_path: str):
        logger.info(f"load preprocess pipeline: {file_path}")
        self.pipeline = load(file_path)
