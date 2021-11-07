from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import List, Optional, Union

import numpy as np
import pandas as pd
from src.dataset.schema import BASE_SCHEMA, X_SCHEMA, XY, Y_SCHEMA, ItemSales
from src.middleware.logger import configure_logger
from src.models.base_model import BaseDemandForecastingModel
from src.models.preprocess import DataPreprocessPipeline

logger = configure_logger(name=__name__)


class Predictor(object):
    def __init__(self):
        pass

    def preprocess(
        self,
        data_preprocess_pipeline: DataPreprocessPipeline,
        raw_df: pd.DataFrame,
        target_year: Optional[int] = None,
        target_week: Optional[int] = None,
        target_items: Optional[List[str]] = None,
        target_stores: Optional[List[str]] = None,
    ):
        weekly_df = data_preprocess_pipeline.preprocess(x=raw_df)

        weekly_target_df = weekly_df[(weekly_df.year == target_year) & (weekly_df.week_of_year == target_week)]
        if target_stores is not None and len(target_stores) > 0:
            weekly_target_df = weekly_target_df[weekly_df.store.isin(target_stores)]
        if target_items is not None and len(target_items) > 0:
            weekly_target_df = weekly_df[weekly_df.item.isin(target_items)]

        logger.info(
            f"""
weekly df columns: {weekly_target_df.columns}
weekly df shape: {weekly_target_df.shape}
    """
        )

        x = data_preprocess_pipeline.transform(x=weekly_target_df)
        x = (
            x[data_preprocess_pipeline.preprocessed_columns]
            .drop(["sales", "store", "item"], axis=1)
            .reset_index(drop=True)
        )
        logger.info(
            f"""
preprocessed df columns: {x.columns}
preprocessed df shape: {x.shape}
    """
        )
        return x

    def predict(
        self,
        model: BaseDemandForecastingModel,
        data_preprocess_pipeline: DataPreprocessPipeline,
        raw_df: pd.DataFrame,
        target_year: Optional[int] = None,
        target_week: Optional[int] = None,
        target_items: Optional[List[str]] = None,
        target_stores: Optional[List[str]] = None,
    ) -> Union[np.ndarray, pd.DataFrame]:
        x = self.preprocess(
            data_preprocess_pipeline=data_preprocess_pipeline,
            raw_df=raw_df,
            target_year=target_year,
            target_week=target_week,
            target_stores=target_stores,
            target_items=target_items,
        )
        predictions = model.predict(x=x)
        return predictions
