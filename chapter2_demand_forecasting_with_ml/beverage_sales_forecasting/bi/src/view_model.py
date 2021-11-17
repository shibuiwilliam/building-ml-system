from datetime import date
from typing import List, Optional

import numpy as np
import pandas as pd
from db_client import AbstractDBClient
from logger import configure_logger
from model import ItemRepository, ItemSales, ItemSalesRepository, RegionRepository, StoreRepository

logger = configure_logger(__name__)


class BaseViewModel(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client


class RegionViewModel(BaseViewModel):
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


class StoreViewModel(BaseViewModel):
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


class ItemViewModel(BaseViewModel):
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


class ItemSalesViewModel(BaseViewModel):
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
df shape: {df.shape}
df columns: {df.columns}
                """
        )
        return df

    def retrieve_weekly_item_sales(daily_df: pd.DataFrame) -> pd.DataFrame:
        weekly_df = (
            daily_df.groupby(
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
df shape: {weekly_df.shape}
df columns: {weekly_df.columns}
                """
        )
        return weekly_df

    def retrieve_monthly_item_sales(daily_df: pd.DataFrame) -> pd.DataFrame:
        monthly_df = (
            daily_df.groupby(
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
df shape: {monthly_df.shape}
df columns: {monthly_df.columns}
                """
        )
        return monthly_df
