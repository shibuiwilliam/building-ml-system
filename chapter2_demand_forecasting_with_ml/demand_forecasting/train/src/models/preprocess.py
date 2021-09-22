import numpy as np
from joblib import dump, load
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class ItemSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return x[[self.key]]


class ItemsSelector(BaseEstimator, TransformerMixin):
    def __init__(self, keys):
        self.keys = keys

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return x[self.keys]


class Log1pTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return np.log1p(x)


class Expm1Transformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        return np.expm1(x)


class DataPreprocessPipeline(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.bare_pipeline = (
            "bare_pipeline",
            Pipeline(
                [
                    (
                        "bare_selector",
                        ItemsSelector(
                            keys=[
                                "is_month_start",
                                "is_month_end",
                            ],
                        ),
                    ),
                    (
                        "bare_simple_imputer",
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
                        "numericals_selector",
                        ItemsSelector(
                            keys=[
                                "item_price",
                                "day_of_year",
                            ],
                        ),
                    ),
                    (
                        "numericals_simple_imputer",
                        SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                    ),
                    (
                        "numericals_standard_scaler",
                        StandardScaler(),
                    ),
                ]
            ),
        )
        self.category_pipeline = (
            "category_pipeline",
            Pipeline(
                [
                    (
                        "categories_selector",
                        ItemsSelector(
                            keys=[
                                "store",
                                "item",
                                "day_of_week",
                                "day_of_month",
                                "week_of_year",
                                "month",
                                "year",
                            ],
                        ),
                    ),
                    (
                        "categories_simple_imputer",
                        SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=None),
                    ),
                    (
                        "categories_one_hot_encoder",
                        OneHotEncoder(sparse=True, handle_unknown="ignore"),
                    ),
                ]
            ),
        )
        self.pipeline: FeatureUnion = FeatureUnion(
            [
                self.numerical_pipeline,
                self.category_pipeline,
                self.bare_pipeline,
            ]
        )

    def fit(self, x, y=None):
        self.pipeline.fit(x)
        return self

    def transform(self, x):
        return self.pipeline.transform(x)

    def fit_transform(self, x, y=None):
        return self.pipeline.fit_transform(x)

    def dump(self, file_path: str):
        dump(self.pipeline, file_path)

    def load(self, file_path: str):
        self.pipeline = load(file_path)


class TargetPreprocessPipeline(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.pipeline: Pipeline = Pipeline(
            [
                (
                    "label_selector",
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
        )

    def fit(self, x, y=None):
        self.pipeline.fit(x)
        return self

    def transform(self, x):
        return self.pipeline.transform(x)

    def fit_transform(self, x, y=None):
        return self.pipeline.fit_transform(x)

    def dump(self, file_path: str):
        dump(self.pipeline, file_path)

    def load(self, file_path: str):
        self.pipeline = load(file_path)
