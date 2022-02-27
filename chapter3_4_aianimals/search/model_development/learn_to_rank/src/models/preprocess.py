import random
import sys
import os
from typing import Dict, List, Optional, Tuple, Union

import cloudpickle
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from src.dataset.schema import RawData, SplitData
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)

cloudpickle.register_pickle_by_value(sys.modules[__name__])


def make_query_id(
    phrases: str,
    animal_category_id: Optional[int],
    animal_subcategory_id: Optional[int],
) -> str:
    return f"{phrases}_{animal_category_id}_{animal_subcategory_id}"


def random_split(
    raw_data: RawData,
    test_size: float = 0.3,
) -> SplitData:
    logger.info("random split")
    x_train, x_test, y_train, y_test = train_test_split(
        raw_data.data,
        raw_data.target,
        test_size=test_size,
        shuffle=True,
    )
    return SplitData(
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
        q_train=None,
        q_test=None,
    )


def split_by_qid(
    raw_data: RawData,
    test_size: float = 0.3,
) -> SplitData:
    logger.info("split by qid")
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    q_train = []
    q_test = []
    _data: Dict[str, List[Tuple]] = {}
    for r, t in zip(raw_data.data, raw_data.target):
        qid = make_query_id(
            phrases=r.query_phrases,
            animal_category_id=r.query_animal_category_id,
            animal_subcategory_id=r.query_animal_subcategory_id,
        )
        if qid in _data.keys():
            _data[qid].append((r, t))
        else:
            _data[qid] = [(r, t)]
    for _, rts in _data.items():
        if len(rts) == 1:
            x_train.append(rts[0][0])
            y_train.append(rts[0][1])
            q_train.append(1)
        else:
            l = len(rts)
            if l > 10000:
                l = 10000
            _rts = random.sample(rts, l)
            train_size = int(l * (1 - test_size))
            for i, rt in enumerate(_rts):
                if i < train_size:
                    x_train.append(rt[0])
                    y_train.append(rt[1])
                else:
                    x_test.append(rt[0])
                    y_test.append(rt[1])
            q_train.append(train_size)
            q_test.append(l - train_size)
    return SplitData(
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
        q_train=q_train,
        q_test=q_test,
    )


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
        x: List[Optional[Union[int, str]]],
    ):
        return self.pipeline.transform(x)

    def fit(
        self,
        x: List[Optional[Union[int, str]]],
        y=None,
    ):
        return self.pipeline.fit(x)

    def fit_transform(
        self,
        x: List[Optional[Union[int, str]]],
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
