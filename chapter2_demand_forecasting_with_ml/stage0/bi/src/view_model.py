from datetime import date
from typing import List, Optional

import numpy as np
import pandas as pd
from logger import configure_logger
from model import (
    ItemRepository,
    ItemSalesRepository,
    ItemWeeklySalesPredictionsRepository,
    StoreRepository,
)

logger = configure_logger(__name__)


class BaseViewModel(object):
    def __init__(self):
        pass


class StoreViewModel(BaseViewModel):
    def __init__(self):
        super().__init__()
        self.store_repository = StoreRepository()

    def list_stores(self) -> List[str]:
        stores = self.store_repository.select()
        store_names = [r.name for r in stores]
        return store_names


class ItemViewModel(BaseViewModel):
    def __init__(self):
        super().__init__()
        self.item_repository = ItemRepository()

    def list_items(self) -> List[str]:
        items = self.item_repository.select()
        item_names = [r.name for r in items]
        return item_names


class ItemSalesViewModel(BaseViewModel):
    def __init__(self):
        super().__init__()
        self.item_sales_repository = ItemSalesRepository()

    def retrieve_item_sales(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        day_of_week: Optional[str] = None,
        item: Optional[str] = None,
        store: Optional[str] = None,
    ) -> pd.DataFrame:
        dataset = self.item_sales_repository.select(
            date_from=date_from,
            date_to=date_to,
            day_of_week=day_of_week,
            item=item,
            store=store,
        )
        df = pd.DataFrame([d.dict() for d in dataset])
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df.date.dt.month
        df["year"] = df.date.dt.year
        df = df.drop("id", axis=1)
        return df

    def retrieve_daily_item_sales(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        day_of_week: Optional[str] = None,
        item: Optional[str] = None,
        store: Optional[str] = None,
    ) -> pd.DataFrame:
        df = self.retrieve_item_sales(
            date_from=date_from,
            date_to=date_to,
            day_of_week=day_of_week,
            item=item,
            store=store,
        )
        logger.info(
            f"""
daily df
    df shape: {df.shape}
    df columns: {df.columns}
                """
        )
        return df

    def retrieve_weekly_item_sales(
        self,
        daily_sales_df: pd.DataFrame,
    ) -> pd.DataFrame:
        weekly_sales_df = (
            daily_sales_df.groupby(
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
                    "total_sales_amount": np.sum,
                }
            )
            .astype(
                {
                    "month": int,
                    "item_price": int,
                    "sales": int,
                    "total_sales_amount": int,
                }
            )
            .reset_index(
                level=[
                    "year",
                    "week_of_year",
                    "store",
                    "item",
                ]
            )
        )
        logger.info(
            f"""
weekly df
    df shape: {weekly_sales_df.shape}
    df columns: {weekly_sales_df.columns}
                """
        )
        return weekly_sales_df

    def retrieve_monthly_item_sales(
        self,
        daily_sales_df: pd.DataFrame,
    ) -> pd.DataFrame:
        monthly_sales_df = (
            daily_sales_df.groupby(
                [
                    "year",
                    "month",
                    "store",
                    "item",
                ]
            )
            .agg(
                {
                    "item_price": np.mean,
                    "sales": np.sum,
                    "total_sales_amount": np.sum,
                }
            )
            .astype(
                {
                    "item_price": int,
                    "sales": int,
                    "total_sales_amount": int,
                }
            )
            .reset_index(
                level=[
                    "year",
                    "month",
                    "store",
                    "item",
                ]
            )
        )
        logger.info(
            f"""
monthly df
    df shape: {monthly_sales_df.shape}
    df columns: {monthly_sales_df.columns}
                """
        )
        return monthly_sales_df


class ItemSalesPredictionEvaluationViewModel(BaseViewModel):
    def __init__(self):
        super().__init__()
        self.item_weekly_sales_predicitons_repository = ItemWeeklySalesPredictionsRepository()

    def aggregate_item_weekly_sales_evaluation(
        self,
        weekly_sales_df: pd.DataFrame,
        item: Optional[str] = None,
        store: Optional[str] = None,
        year: Optional[int] = None,
        week_of_year: Optional[int] = None,
    ) -> pd.DataFrame:
        item_weekly_sales_predictions = self.item_weekly_sales_predicitons_repository.select(
            item=item,
            store=store,
            year=year,
            week_of_year=week_of_year,
        )
        weekly_sales_predictions_df = pd.DataFrame([d.dict() for d in item_weekly_sales_predictions])
        logger.info(
            f"""
weekly prediction df
    df shape: {weekly_sales_predictions_df.shape}
    df columns: {weekly_sales_predictions_df.columns}
                """
        )
        weekly_sales_evaluation_df = pd.merge(
            weekly_sales_df,
            weekly_sales_predictions_df,
            on=["year", "week_of_year", "store", "item"],
            how="inner",
        )
        weekly_sales_evaluation_df["diff"] = (
            weekly_sales_evaluation_df["sales"].astype("float") - weekly_sales_evaluation_df["prediction"]
        )
        weekly_sales_evaluation_df["error_rate"] = weekly_sales_evaluation_df["diff"] / weekly_sales_evaluation_df[
            "sales"
        ].astype("float")
        weekly_sales_evaluation_df = weekly_sales_evaluation_df[
            [
                "year",
                "month",
                "week_of_year",
                "store",
                "item",
                "item_price",
                "sales",
                "prediction",
                "diff",
                "error_rate",
                "predicted_at",
            ]
        ]
        return weekly_sales_evaluation_df
