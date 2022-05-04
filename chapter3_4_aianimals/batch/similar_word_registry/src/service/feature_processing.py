import sys
from typing import List

import cloudpickle
import MeCab
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from src.constants import STOP_WORDS
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)

cloudpickle.register_pickle_by_value(sys.modules[__name__])


class CategoricalVectorizer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        sparse: bool = True,
        handle_unknown: str = "ignore",
    ):
        self.sparse = sparse
        self.handle_unknown = handle_unknown
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
                        fill_value=-1,
                    ),
                ),
                (
                    "one_hot_encoder",
                    OneHotEncoder(
                        sparse=self.sparse,
                        handle_unknown=self.handle_unknown,
                    ),
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


class DescriptionTokenizer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        stop_words=STOP_WORDS,
    ):
        self.stop_words = stop_words
        self.tokenizer = MeCab.Tagger()

    def tokenize_description(
        self,
        text: str,
        stop_words: List[str] = [],
    ) -> List[str]:
        ts = self.tokenizer.parse(text)
        ts = ts.split("\n")
        tokens = []
        for t in ts:
            if t == "EOS":
                break
            s = t.split("\t")
            r = s[1].split(",")
            w = ""
            if r[0] == "名詞":
                w = s[0]
            elif r[0] in ("動詞", "形容詞"):
                w = r[6]
            if w == "":
                continue
            if w in stop_words:
                continue
            tokens.append(w)
        return tokens

    def transform(
        self,
        X: List[str],
    ) -> np.ndarray:
        y = []
        for x in X:
            ts = self.tokenize_description(
                text=x,
                stop_words=self.stop_words,
            )
            ts = " ".join(ts)
            y.append(ts)
        return np.array(y)

    def fit(
        self,
        X: List[str],
        y=None,
    ):
        return self

    def fit_transform(
        self,
        X: List[str],
        y=None,
    ) -> np.ndarray:
        self.fit(X=X, y=y)
        return self.transform(X=X)


class NameTokenizer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        stop_words=STOP_WORDS,
    ):
        self.stop_words = stop_words
        self.tokenizer = MeCab.Tagger()

    def tokenize_name(
        self,
        text: str,
        stop_words: List[str] = [],
    ) -> List[str]:
        ts = self.tokenizer.parse(text)
        ts = ts.split("\n")
        tokens = []
        for t in ts:
            if t == "EOS":
                break
            s = t.split("\t")
            r = s[1].split(",")
            w = s[0]
            if r[0] in ("助詞"):
                continue
            if w == "":
                continue
            if w in stop_words:
                continue
            tokens.append(w)
        return tokens

    def transform(
        self,
        X: List[str],
    ) -> np.ndarray:
        y = []
        for x in X:
            ts = self.tokenize_name(
                text=x,
                stop_words=self.stop_words,
            )
            ts = " ".join(ts)
            y.append(ts)
        return np.array(y)

    def fit(
        self,
        X: List[str],
        y=None,
    ):
        return self

    def fit_transform(
        self,
        X: List[str],
        y=None,
    ) -> np.ndarray:
        self.fit(X=X, y=y)
        return self.transform(X=X)


class DescriptionVectorizer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        max_features: int = 500,
    ):
        self.max_features = max_features
        self.define_pipeline()

    def define_pipeline(self):
        self.pipeline = Pipeline(
            [
                (
                    "description_tfids_vectorizer",
                    TfidfVectorizer(max_features=self.max_features),
                ),
            ]
        )

    def transform(
        self,
        X: List[List[str]],
    ):
        return self.pipeline.transform(X)

    def fit(
        self,
        X: List[List[str]],
        y=None,
    ):
        return self.pipeline.fit(X=X, y=y)

    def fit_transform(
        self,
        X: List[List[str]],
        y=None,
    ):
        return self.pipeline.fit_transform(X=X, y=y)


class NameVectorizer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        max_features: int = 300,
    ):
        self.max_features = max_features
        self.define_pipeline()

    def define_pipeline(self):
        self.pipeline = Pipeline(
            [
                (
                    "name_tfids_vectorizer",
                    TfidfVectorizer(max_features=self.max_features),
                ),
            ]
        )

    def transform(
        self,
        X: List[List[str]],
    ):
        return self.pipeline.transform(X)

    def fit(
        self,
        X: List[List[str]],
        y=None,
    ):
        return self.pipeline.fit(X=X, y=y)

    def fit_transform(
        self,
        X: List[List[str]],
        y=None,
    ):
        return self.pipeline.fit_transform(X=X, y=y)
