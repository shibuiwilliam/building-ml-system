from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from src.dataset.schema import BASE_SCHEMA, WEEKLY_PREDICTION_SCHEMA, X_SCHEMA
from src.middleware.logger import configure_logger
from src.models.base_model import BaseDemandForecastingModel
from src.models.preprocess import DataPreprocessPipeline

logger = configure_logger(name=__name__)


class Predictor(object):
    def __init__(self):
        pass

    def filter(
        self,
        raw_df: pd.DataFrame,
        target_year: Optional[int] = None,
        target_week: Optional[int] = None,
        target_items: Optional[List[str]] = None,
        target_stores: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        raw_df = raw_df[(raw_df.year == target_year) & (raw_df.week_of_year == target_week)]
        if target_stores is not None and len(target_stores) > 0:
            raw_df = raw_df[raw_df.store.isin(target_stores)]
        if target_items is not None and len(target_items) > 0:
            raw_df = raw_df[raw_df.item.isin(target_items)]
        logger.info(
            f"""
filtered df columns: {raw_df.columns}
filtered df shape: {raw_df.shape}
    """
        )
        return raw_df

    def postprocess(
        self,
        df: pd.DataFrame,
        predictions: np.ndarray,
    ) -> pd.DataFrame:
        df = df[["year", "week_of_year", "store", "item", "item_price"]]
        df["prediction"] = predictions
        df = WEEKLY_PREDICTION_SCHEMA.validate(df)
        logger.info(
            f"""
predicted df columns: {df.columns}
predicted df shape: {df.shape}
    """
        )
        return df

    def predict(
        self,
        model: BaseDemandForecastingModel,
        data_preprocess_pipeline: DataPreprocessPipeline,
        raw_df: pd.DataFrame,
        target_year: Optional[int] = None,
        target_week: Optional[int] = None,
        target_items: Optional[List[str]] = None,
        target_stores: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        raw_df = BASE_SCHEMA.validate(raw_df)
        logger.info(
            f"""
raw df columns: {raw_df.columns}
raw df shape: {raw_df.shape}
    """
        )
        weekly_df = data_preprocess_pipeline.preprocess(x=raw_df)
        x = data_preprocess_pipeline.transform(x=weekly_df)

        x = self.filter(
            raw_df=x,
            target_year=target_year,
            target_week=target_week,
            target_stores=target_stores,
            target_items=target_items,
        )
        x_test = (
            x[data_preprocess_pipeline.preprocessed_columns]
            .drop(["sales", "store", "item"], axis=1)
            .reset_index(drop=True)
        )
        x_test = X_SCHEMA.validate(x_test)
        predictions = model.predict(x=x_test)

        weekly_df = self.filter(
            raw_df=weekly_df,
            target_year=target_year,
            target_week=target_week,
            target_stores=target_stores,
            target_items=target_items,
        )
        weekly_prediction = self.postprocess(
            df=weekly_df,
            predictions=predictions,
        )
        return weekly_prediction
