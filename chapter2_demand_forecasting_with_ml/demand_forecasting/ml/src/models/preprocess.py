import random
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import BaseCrossValidator
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler, OneHotEncoder
from src.dataset.schema import BASE_SCHEMA, MONTHS, PREPROCESSED_SCHEMA, WEEKLY_SCHEMA, WEEKS, YEARS
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


def select_by_store_and_item(
    df: pd.DataFrame,
    stores: Optional[List[str]] = None,
    items: Optional[List[str]] = None,
) -> pd.DataFrame:
    if stores is not None:
        logger.info(f"stores to be used: {stores}")
        df = df[df["store"].isin(stores)]
    if items is not None:
        logger.info(f"items to be used: {items}")
        df = df[df["item"].isin(items)]
    return df


class WeekBasedSplit(BaseCrossValidator):
    def __init__(
        self,
        n_splits: int = 3,
        gap: int = 2,
        min_train_size_rate: float = 0.7,
        columns: Dict = None,
        types: Dict = None,
    ):
        if min_train_size_rate >= 1.0:
            raise ValueError
        self.n_splits = n_splits
        self.gap = gap
        self.min_train_size_rate = min_train_size_rate
        self.columns = columns
        self.types = types

    def split(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        y=None,
        groups=None,
    ):
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X, columns=self.columns).astype(self.types)
        year_weeks = X.year.astype(str).str.cat(X.week_of_year.astype(str), sep="_").unique()
        year_week_index = [i for i in range(len(year_weeks))]
        x_size = len(year_week_index)
        min_train_size = int(x_size * self.min_train_size_rate)
        candidates = year_week_index[self.gap + min_train_size : -self.gap]
        for _ in range(self.n_splits):
            train_position = random.choice(candidates)
            train_year_week = year_weeks[train_position]
            _train_year, _train_week = train_year_week.split("_")
            train_year, train_week = int(_train_year), int(_train_week)

            test_position = train_position + self.gap
            test_year_week = year_weeks[test_position]
            _test_year, _test_week = test_year_week.split("_")
            test_year, test_week = int(_test_year), int(_test_week)

            x_train = X[(X.year < train_year) | ((X.year == train_year) & (X.week_of_year <= train_week))]
            x_test = X[(X.year > test_year) | ((X.year == test_year) & (X.week_of_year >= test_week))]

            yield np.array(list(x_train.index)), np.array(list(x_test.index))

    def get_n_splits(
        self,
        X,
        y=None,
        groups=None,
    ):
        return self.n_splits


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
    def dump_pipeline(
        self,
        file_path: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def load_pipeline(
        self,
        file_path: str,
    ):
        raise NotImplementedError


class DataPreprocessPipeline(BasePreprocessPipeline):
    def __init__(self):
        self.pipeline: Union[Pipeline, ColumnTransformer] = None

        self.week_of_year_ohe_transformer: FunctionTransformer = None
        self.month_ohe_transformer: FunctionTransformer = None
        self.year_ohe_transformer: FunctionTransformer = None

        self.bare_columns = ["store", "item", "year", "week_of_year", "sales"]
        self.lag_columns: List[str] = [f"sales_lag_{i}" for i in range(2, 54, 1)]
        self.store_categories: List[str] = []
        self.item_categories: List[str] = []
        self.week_of_year_categories: List[str] = []
        self.month_categories: List[str] = []
        self.year_categories: List[str] = []
        self.preprocessed_columns: List[str] = []
        self.preprocessed_types: Dict[str, str] = {}

        self.define_pipeline()

    def define_pipeline(self):
        logger.info("init pipeline")
        week_of_year_ohe = OneHotEncoder(sparse=True, handle_unknown="ignore").fit([[i] for i in WEEKS])
        month_ohe = OneHotEncoder(sparse=True, handle_unknown="ignore").fit([[i] for i in MONTHS])
        year_ohe = OneHotEncoder(sparse=True, handle_unknown="ignore").fit([[i] for i in YEARS])

        self.week_of_year_categories = [f"week_of_year_{c}" for c in week_of_year_ohe.categories_[0].tolist()]
        self.month_categories = [f"month_{c}" for c in month_ohe.categories_[0].tolist()]
        self.year_categories = [f"year_{c}" for c in year_ohe.categories_[0].tolist()]

        self.week_of_year_ohe_transformer = FunctionTransformer(week_of_year_ohe.transform)
        self.month_ohe_transformer = FunctionTransformer(month_ohe.transform)
        self.year_ohe_transformer = FunctionTransformer(year_ohe.transform)

        self.pipeline = ColumnTransformer(
            [
                (
                    "bare",
                    Pipeline(
                        [
                            (
                                "simple_imputer",
                                SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                            )
                        ]
                    ),
                    self.bare_columns,
                ),
                (
                    "lag",
                    Pipeline(
                        [
                            (
                                "simple_imputer",
                                SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                            )
                        ]
                    ),
                    self.lag_columns,
                ),
                (
                    "numerical",
                    Pipeline(
                        [
                            (
                                "simple_imputer",
                                SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                            ),
                            ("scaler", MinMaxScaler()),
                        ]
                    ),
                    ["item_price"],
                ),
                (
                    "categorical",
                    Pipeline(
                        [
                            (
                                "simple_imputer",
                                SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                            ),
                            ("one_hot_encoder", OneHotEncoder(sparse=True, handle_unknown="ignore")),
                        ]
                    ),
                    ["store", "item"],
                ),
                (
                    "week_of_year",
                    Pipeline(
                        [
                            (
                                "simple_imputer",
                                SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                            ),
                            ("one_hot_encoder", FunctionTransformer(week_of_year_ohe.transform)),
                        ]
                    ),
                    ["week_of_year"],
                ),
                (
                    "month",
                    Pipeline(
                        [
                            (
                                "simple_imputer",
                                SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                            ),
                            ("one_hot_encoder", FunctionTransformer(month_ohe.transform)),
                        ]
                    ),
                    ["month"],
                ),
                (
                    "year",
                    Pipeline(
                        [
                            (
                                "simple_imputer",
                                SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                            ),
                            ("one_hot_encoder", FunctionTransformer(year_ohe.transform)),
                        ]
                    ),
                    ["year"],
                ),
            ],
            verbose_feature_names_out=True,
        )
        logger.info(f"pipeline: {self.pipeline}")

    def preprocess(
        self,
        x: pd.DataFrame,
        y=None,
    ) -> pd.DataFrame:
        x = BASE_SCHEMA.validate(x)
        x["year"] = x.date.dt.year
        x["week_of_year"] = x.date.dt.weekofyear
        x["month"] = x.date.dt.month
        weekly_df = (
            x.groupby(["year", "week_of_year", "store", "item"])
            .agg(
                {
                    "month": np.mean,
                    "item_price": np.mean,
                    "sales": np.sum,
                    "total_sales": np.sum,
                }
            )
            .astype(
                {
                    "month": int,
                    "item_price": int,
                    "sales": int,
                    "total_sales": int,
                }
            )
        )
        weekly_df = weekly_df.reset_index(level=["year", "week_of_year", "store", "item"])
        weekly_df = weekly_df.sort_values(["year", "month", "week_of_year", "store", "item"])
        for i in range(2, 54, 1):
            weekly_df[f"sales_lag_{i}"] = weekly_df.groupby(["store", "item"])["sales"].shift(i)
        weekly_df = WEEKLY_SCHEMA.validate(weekly_df)
        return weekly_df

    def fit(
        self,
        x: pd.DataFrame,
        y=None,
    ):
        if self.pipeline is None:
            raise AttributeError
        x = WEEKLY_SCHEMA.validate(x)
        self.pipeline.fit(x)

        self.set_categories()

        return self

    def transform(
        self,
        x: pd.DataFrame,
    ) -> pd.DataFrame:
        if self.pipeline is None:
            raise AttributeError
        x = WEEKLY_SCHEMA.validate(x)
        _x = self.pipeline.transform(x)
        df = self.postprocess(x=_x)
        return df

    def fit_transform(
        self,
        x: pd.DataFrame,
        y=None,
    ) -> np.ndarray:
        if self.pipeline is None:
            raise AttributeError
        x = WEEKLY_SCHEMA.validate(x)
        _x = self.pipeline.fit_transform(x)

        self.set_categories()

        df = self.postprocess(x=_x)
        return df

    def set_categories(self):
        self.store_categories = [
            f"store_{c}" for c in self.pipeline.named_transformers_["categorical"].steps[-1][-1].categories_[0].tolist()
        ]
        self.item_categories = [
            f"item_{c}" for c in self.pipeline.named_transformers_["categorical"].steps[-1][-1].categories_[1].tolist()
        ]
        logger.info(f"store_categories: {self.store_categories}")
        logger.info(f"item_categories: {self.item_categories}")

    def postprocess(
        self,
        x: np.ndarray,
    ) -> pd.DataFrame:
        self.preprocessed_columns = []
        self.preprocessed_columns.extend(self.bare_columns)
        self.preprocessed_columns.extend(self.lag_columns)
        self.preprocessed_columns.append("item_price")
        self.preprocessed_columns.extend(self.store_categories)
        self.preprocessed_columns.extend(self.item_categories)
        self.preprocessed_columns.extend(self.week_of_year_categories)
        self.preprocessed_columns.extend(self.month_categories)
        self.preprocessed_columns.extend(self.year_categories)
        self.preprocessed_types = {c: "float64" for c in self.preprocessed_columns}
        self.preprocessed_types["store"] = "str"
        self.preprocessed_types["item"] = "str"
        self.preprocessed_types["year"] = "int"
        self.preprocessed_types["week_of_year"] = "int"
        logger.info(f"preprocessed_columns: {self.preprocessed_columns}")
        logger.info(f"preprocessed_types: {self.preprocessed_types}")
        df = pd.DataFrame(x, columns=self.preprocessed_columns).astype(self.preprocessed_types)
        df = PREPROCESSED_SCHEMA.validate(df)
        return df

    def dump_pipeline(
        self,
        file_path: str,
    ):
        logger.info(f"save preprocess pipeline: {file_path}")
        dump(self.pipeline, file_path)

    def load_pipeline(
        self,
        file_path: str,
    ):
        logger.info(f"load preprocess pipeline: {file_path}")
        self.pipeline = load(file_path)
