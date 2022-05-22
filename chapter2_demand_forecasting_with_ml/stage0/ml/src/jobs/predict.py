from typing import List, Optional

import numpy as np
import pandas as pd
from src.dataset.schema import (
    BASE_SCHEMA,
    PREPROCESSED_SCHEMA,
    RAW_PREDICTION_SCHEMA,
    WEEKLY_PREDICTION_SCHEMA,
    X_SCHEMA,
)
from src.middleware.logger import configure_logger
from src.models.base_model import BaseDemandForecastingModel
from src.models.preprocess import DataPreprocessPipeline

logger = configure_logger(name=__name__)


class Predictor(object):
    def __init__(self):
        pass

    def filter(
        self,
        df: pd.DataFrame,
        target_year: int,
        target_week: int,
        target_items: Optional[List[str]] = None,
        target_stores: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        logger.info("filter data")
        df = df[(df.year == target_year) & (df.week_of_year == target_week)]
        if target_stores is not None and len(target_stores) > 0:
            df = df[df.store.isin(target_stores)]
        if target_items is not None and len(target_items) > 0:
            df = df[df.item.isin(target_items)]
        logger.info(
            f"""
Filtered prediction target data
filtered df columns: {df.columns}
filtered df shape: {df.shape}
date from: {df.date.min()}
date to: {df.date.max()}
    """
        )
        return df

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
        previous_df: pd.DataFrame,
        data_to_be_predicted_df: pd.DataFrame,
        target_year: int,
        target_week: int,
        target_items: Optional[List[str]] = None,
        target_stores: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        previous_df = BASE_SCHEMA.validate(previous_df)
        data_to_be_predicted_df = RAW_PREDICTION_SCHEMA.validate(data_to_be_predicted_df)
        logger.info(
            f"""
target_year: {target_year}
target_week: {target_week}
target_items: {'ALL' if target_items is None else target_items}
target_stores: {'ALL' if target_stores is None else target_stores}
    """
        )
        df = pd.concat([previous_df, data_to_be_predicted_df])

        weekly_df = data_preprocess_pipeline.preprocess(x=df)
        x = data_preprocess_pipeline.transform(x=weekly_df)

        x = self.filter(
            df=x,
            target_year=target_year,
            target_week=target_week,
            target_stores=target_stores,
            target_items=target_items,
        )
        x = PREPROCESSED_SCHEMA.validate(x)
        x = (
            x[data_preprocess_pipeline.preprocessed_columns]
            .drop(["sales", "store", "item"], axis=1)
            .reset_index(drop=True)
        )
        x = X_SCHEMA.validate(x)
        predictions = model.predict(x=x)

        weekly_df = self.filter(
            df=weekly_df,
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
