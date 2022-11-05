from datetime import date
from typing import List, Optional

import numpy as np
import pandas as pd
from db_client import AbstractDBClient
from logger import configure_logger
from model import (
    ItemRepository,
    ItemSalesRepository,
    ItemWeeklySalesPredictionsRepository,
    RegionRepository,
    StoreRepository,
)
from schema import ItemSales, ItemWeeklySalesPredictions, YearWeek

logger = configure_logger(__name__)


class BaseService(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client


class RegionService(BaseService):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.region_repository = RegionRepository(db_client=db_client)

    def list_regions(self) -> List[str]:
        regions = self.region_repository.select()
        region_names = [r.name for r in regions]
        return region_names


class StoreService(BaseService):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.store_repository = StoreRepository(db_client=db_client)

    def list_stores(
        self,
        region: Optional[str] = None,
    ) -> List[str]:
        stores = self.store_repository.select(region=region)
        store_names = [r.name for r in stores]
        return store_names


class ItemService(BaseService):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.item_repository = ItemRepository(db_client=db_client)

    def list_items(self) -> List[str]:
        items = self.item_repository.select()
        item_names = [r.name for r in items]
        return item_names


class ItemSalesService(BaseService):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.item_sales_repository = ItemSalesRepository(db_client=db_client)

    def list_item_sales(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        day_of_week: Optional[str] = None,
        item: Optional[str] = None,
        store: Optional[str] = None,
        region: Optional[str] = None,
    ) -> List[ItemSales]:
        item_sales = []
        limit = 10000
        offset = 0
        while True:
            records = self.item_sales_repository.select(
                date_from=date_from,
                date_to=date_to,
                day_of_week=day_of_week,
                item=item,
                store=store,
                region=region,
                limit=limit,
                offset=offset,
            )
            if len(records) == 0:
                logger.info(f"done loading {len(item_sales)} records")
                break
            item_sales.extend(records)
            offset += limit
            logger.info(f"found {len(item_sales)} records...")
        return item_sales

    def retrieve_item_sales(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        day_of_week: Optional[str] = None,
        item: Optional[str] = None,
        store: Optional[str] = None,
        region: Optional[str] = None,
    ) -> pd.DataFrame:
        dataset = self.list_item_sales(
            date_from=date_from,
            date_to=date_to,
            day_of_week=day_of_week,
            item=item,
            store=store,
            region=region,
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
        region: Optional[str] = None,
    ) -> pd.DataFrame:
        df = self.retrieve_item_sales(
            date_from=date_from,
            date_to=date_to,
            day_of_week=day_of_week,
            item=item,
            store=store,
            region=region,
        )
        logger.info(
            f"""
daily df
    df shape: {df.shape}
    df columns: {df.columns}
                """
        )
        logger.info(df)
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
                    "region",
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
                    "region",
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
        logger.info(weekly_sales_df)
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
                    "region",
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
                    "region",
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
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.item_weekly_sales_predicitons_repository = ItemWeeklySalesPredictionsRepository(db_client=db_client)

    def list_item_weekly_sales_predictions(
        self,
        item: Optional[str] = None,
        store: Optional[str] = None,
        region: Optional[str] = None,
        year: Optional[int] = None,
        week_of_year: Optional[int] = None,
        version: int = 0,
    ) -> List[ItemWeeklySalesPredictions]:
        item_weekly_sales_predictions = []
        limit = 10000
        offset = 0
        while True:
            records = self.item_weekly_sales_predicitons_repository.select(
                item=item,
                store=store,
                region=region,
                year=year,
                week_of_year=week_of_year,
                version=version,
                limit=limit,
                offset=offset,
            )
            if len(records) == 0:
                logger.info(f"done loading {len(item_weekly_sales_predictions)} records")
                break
            item_weekly_sales_predictions.extend(records)
            offset += limit
            logger.info(f"found {len(item_weekly_sales_predictions)} records...")
        return item_weekly_sales_predictions

    def list_predicted_unique_year_week(self) -> List[YearWeek]:
        data = self.item_weekly_sales_predicitons_repository.select_unique_year_week()
        return data

    def aggregate_item_weekly_sales_evaluation(
        self,
        weekly_sales_df: pd.DataFrame,
        item: Optional[str] = None,
        store: Optional[str] = None,
        region: Optional[str] = None,
        year: Optional[int] = None,
        week_of_year: Optional[int] = None,
        version: int = 0,
    ) -> Optional[pd.DataFrame]:
        item_weekly_sales_predictions = self.list_item_weekly_sales_predictions(
            item=item,
            store=store,
            region=region,
            year=year,
            week_of_year=week_of_year,
            version=version,
        )
        if len(item_weekly_sales_predictions) == 0:
            return None

        weekly_sales_predictions_df = (
            pd.DataFrame([d.dict() for d in item_weekly_sales_predictions])
            .drop("id", axis=1)
            .drop("region", axis=1)
            .drop("predicted_at", axis=1)
            .drop("version", axis=1)
        )
        logger.info(
            f"""
weekly prediction df
    df shape: {weekly_sales_predictions_df.shape}
    df columns: {weekly_sales_predictions_df.columns}
"""
        )
        logger.info(weekly_sales_predictions_df)
        weekly_sales_evaluation_df = pd.merge(
            weekly_sales_df,
            weekly_sales_predictions_df,
            on=["year", "week_of_year", "store", "item"],
            how="inner",
        )
        logger.info(weekly_sales_evaluation_df)
        weekly_sales_evaluation_df["diff"] = (
            weekly_sales_evaluation_df.sales.astype("float") - weekly_sales_evaluation_df.prediction
        )

        weekly_sales_evaluation_df["error_rate"] = weekly_sales_evaluation_df[
            "diff"
        ] / weekly_sales_evaluation_df.sales.astype("float")
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
        logger.info(
            f"""
weekly sales evaluation df
    df shape: {weekly_sales_evaluation_df.shape}
    df columns: {weekly_sales_evaluation_df.columns}
"""
        )
        return weekly_sales_evaluation_df
