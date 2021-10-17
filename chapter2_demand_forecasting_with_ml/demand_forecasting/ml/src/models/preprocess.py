from abc import ABC, abstractmethod
from typing import List, Optional, Union

import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler, OneHotEncoder
from src.dataset.schema import BASE_SCHEMA, MONTHS, WEEKLY_SCHEMA, WEEKS, YEARS
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

        self.lag_columns: List[str] = [f"sales_lag_{i}" for i in range(1, 54, 1)]
        self.store_categories: List[str] = []
        self.item_categories: List[str] = []
        self.week_of_year_categories: List[str] = []
        self.month_categories: List[str] = []
        self.year_categories: List[str] = []
        self.preprocessed_columns: List[str] = []

    def define_pipeline(self):
        week_of_year_ohe = OneHotEncoder(sparse=True, handle_unknown="ignore").fit(WEEKS)
        month_ohe = OneHotEncoder(sparse=True, handle_unknown="ignore").fit(MONTHS)
        year_ohe = OneHotEncoder(sparse=True, handle_unknown="ignore").fit(YEARS)

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
                        [("simple_imputer", SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None))]
                    ),
                    ["store", "item"],
                ),
                (
                    "sales",
                    Pipeline([("log1p_transformer", Log1pTransformer())]),
                    ["sales"],
                ),
                (
                    "lags",
                    Pipeline([("log1p_transformer", Log1pTransformer())]),
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
                            ("standard_scaler", MinMaxScaler()),
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

    def to_weekly_data(
        self,
        x: pd.DataFrame,
        y=None,
    ) -> pd.DataFrame:
        x = BASE_SCHEMA.validate(x)
        x["year"] = x.date.dt.year
        x["week_of_year"] = x.date.dt.weekofyear
        x["month"] = x.date.dt.month
        df_week = (
            x.groupby(
                [
                    "year",
                    "week_of_year",
                    "store",
                    "item",
                ]
            )
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
        df_week = df_week.reset_index(level=["year", "week_of_year", "store", "item"])
        df_week = df_week.sort_values(["year", "month", "week_of_year", "store", "item"])
        for i in range(1, 54, 1):
            df_week[f"sales_lag_{i}"] = df_week.groupby(["store", "item"])["sales"].shift(i)
        df_week = WEEKLY_SCHEMA.validate(df_week)
        return df_week

    def postprocess(
        self,
        x: np.ndarray,
    ) -> pd.DataFrame:
        self.store_categories = [
            f"store_{c}"
            for c in self.pipelines.named_transformers_["categorical"].steps[-1][-1].categories_[0].tolist()
        ]
        self.item_categories = [
            f"item_{c}" for c in self.pipelines.named_transformers_["categorical"].steps[-1][-1].categories_[1].tolist()
        ]
        self.preprocessed_columns = ["store", "item", "sales"]
        self.preprocessed_columns.extend(self.lag_columns)
        self.preprocessed_columns.append("item_price")
        self.preprocessed_columns.extend(self.store_categories)
        self.preprocessed_columns.extend(self.item_categories)
        self.preprocessed_columns.extend(self.week_of_year_categories)
        self.preprocessed_columns.extend(self.month_categories)
        self.preprocessed_columns.extend(self.year_categories)
        types = {c: "float64" for c in self.preprocessed_columns}
        types["store"] = "str"
        types["item"] = "str"
        df = pd.DataFrame(x, columns=self.preprocessed_columns).astype(types)
        return df

    def fit(
        self,
        x: pd.DataFrame,
        y=None,
    ):
        if self.pipeline is None:
            raise AttributeError
        x = WEEKLY_SCHEMA.validate(x)
        self.pipeline.fit(x)
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
        df = self.postprocess(x=_x)
        return df

    def inverse_transform_target(
        self,
        y: pd.DataFrame,
    ) -> pd.DataFrame:
        return Expm1Transformer().fit_transform(y)

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
