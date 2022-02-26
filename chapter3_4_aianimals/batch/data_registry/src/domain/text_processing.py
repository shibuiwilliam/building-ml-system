import sys
from typing import List

import cloudpickle
import MeCab
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from src.constants import STOP_WORDS
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)

cloudpickle.register_pickle_by_value(sys.modules[__name__])


class DescriptionTokenizer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        stop_words=STOP_WORDS,
    ):
        self.stop_words = stop_words
        self.is_fitted = False

    def tokenize_description(
        self,
        text: str,
        stop_words: List[str] = [],
    ) -> List[str]:
        tokenizer = MeCab.Tagger()
        ts = tokenizer.parse(text)
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

    def transform(self, X) -> np.ndarray:
        y = []
        for x in X:
            ts = self.tokenize_description(
                text=x,
                stop_words=self.stop_words,
            )
            ts = " ".join(ts)
            y.append(ts)
        return np.array(y)

    def fit(self, X, y=None):
        self.is_fitted = True
        return self

    def fit_transform(self, X, y=None) -> np.ndarray:
        self.fit(X=X, y=y)
        return self.transform(X=X)


class NameTokenizer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        stop_words=STOP_WORDS,
    ):
        self.stop_words = stop_words
        self.is_fitted = False

    def tokenize_name(
        self,
        text: str,
        stop_words: List[str] = [],
    ) -> List[str]:
        tokenizer = MeCab.Tagger()
        ts = tokenizer.parse(text)
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

    def transform(self, X) -> np.ndarray:
        y = []
        for x in X:
            ts = self.tokenize_name(
                text=x,
                stop_words=self.stop_words,
            )
            ts = " ".join(ts)
            y.append(ts)
        return np.array(y)

    def fit(self, X, y=None):
        self.is_fitted = True
        return self

    def fit_transform(self, X, y=None) -> np.ndarray:
        self.fit(X=X, y=y)
        return self.transform(X=X)


class DescriptionVectorizer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        stop_words: List[str] = STOP_WORDS,
        max_features: int = 500,
    ):
        self.stop_words = stop_words
        self.max_features = max_features
        self.define_pipeline()
        self.is_fitted = False

    def define_pipeline(self):
        self.pipeline = Pipeline(
            [
                (
                    "description_tokenizer",
                    DescriptionTokenizer(stop_words=self.stop_words),
                ),
                (
                    "description_tfids_vectorizer",
                    TfidfVectorizer(max_features=self.max_features),
                ),
            ]
        )

    def transform(self, X):
        return self.pipeline.transform(X)

    def fit(self, X, y=None):
        self.is_fitted = True
        return self.pipeline.fit(X=X, y=y)

    def fit_transform(self, X, y=None):
        return self.pipeline.fit_transform(X=X, y=y)


class NameVectorizer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        stop_words: List[str] = STOP_WORDS,
        max_features: int = 300,
    ):
        self.stop_words = stop_words
        self.max_features = max_features
        self.define_pipeline()
        self.is_fitted = False

    def define_pipeline(self):
        self.pipeline = Pipeline(
            [
                (
                    "name_tokenizer",
                    DescriptionTokenizer(stop_words=self.stop_words),
                ),
                (
                    "name_tfids_vectorizer",
                    TfidfVectorizer(max_features=self.max_features),
                ),
            ]
        )

    def transform(self, X):
        return self.pipeline.transform(X)

    def fit(self, X, y=None):
        self.is_fitted = True
        return self.pipeline.fit(X=X, y=y)

    def fit_transform(self, X, y=None):
        return self.pipeline.fit_transform(X=X, y=y)
