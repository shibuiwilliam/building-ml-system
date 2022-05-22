from datetime import date
from typing import List, Optional

import numpy as np
import pandas as pd
from logger import configure_logger
from model import Container, ItemRepository, ItemSalesRepository, ItemWeeklySalesPredictionsRepository, StoreRepository

logger = configure_logger(__name__)


class BaseService(object):
    def __init__(self):
        pass


class StoreService(BaseService):
    def __init__(self):
        super().__init__()
        self.store_repository = StoreRepository()

    def list_stores(
        self,
        container: Container,
    ) -> List[str]:
        stores = self.store_repository.select(container=container)
        store_names = [r.name for r in stores]
        return store_names


class ItemService(BaseService):
    def __init__(self):
        super().__init__()
        self.item_repository = ItemRepository()

    def list_items(
        self,
        container: Container,
    ) -> List[str]:
        items = self.item_repository.select(container=container)
        item_names = [r.name for r in items]
        return item_names


class ItemSalesService(BaseService):
    def __init__(self):
        super().__init__()
        self.item_sales_repository = ItemSalesRepository()

    def retrieve_item_sales(
        self,
        container: Container,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        day_of_week: Optional[str] = None,
        item: Optional[str] = None,
        store: Optional[str] = None,
    ) -> pd.DataFrame:
        df = self.item_sales_repository.select(
            container=container,
            date_from=date_from,
            date_to=date_to,
            day_of_week=day_of_week,
            item=item,
            store=store,
        )
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df.date.dt.month
        df["year"] = df.date.dt.year
        return df

    def retrieve_daily_item_sales(
        self,
        container: Container,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        day_of_week: Optional[str] = None,
        item: Optional[str] = None,
        store: Optional[str] = None,
    ) -> pd.DataFrame:
        df = self.retrieve_item_sales(
            container=container,
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
        daily_sales_df["month"] = daily_sales_df.date.dt.month
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


class ItemSalesPredictionEvaluationService(BaseService):
    def __init__(self):
        super().__init__()
        self.item_weekly_sales_predicitons_repository = ItemWeeklySalesPredictionsRepository()

    def aggregate_item_weekly_sales_evaluation(
        self,
        container: Container,
        weekly_sales_df: pd.DataFrame,
        item: Optional[str] = None,
        store: Optional[str] = None,
    ) -> pd.DataFrame:
        weekly_sales_predictions_df = self.item_weekly_sales_predicitons_repository.select(
            container=container,
            item=item,
            store=store,
        )
        weekly_sales_predictions_df = weekly_sales_predictions_df.drop("item_price", axis=1)
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
            ]
        ]
        return weekly_sales_evaluation_df
