from datetime import date
from typing import Dict, List, Optional

import pandas as pd
from constants import TABLES
from logger import configure_logger
from schema import Item, ItemSales, ItemWeeklySalesPredictions, Region, Store, BASE_SCHEMA

logger = configure_logger(__name__)


class Container(object):
    def __init__(self):
        self.sales_df: pd.DataFrame = None
        self.prediction_dict: Dict[int, Dict[int, pd.DataFrame]] = {}

    def load_df(
        self,
        file_path: str,
    ) -> pd.DataFrame:
        return pd.read_csv(file_path)

    def load_sales_df(
        self,
        file_path: str,
    ):
        self.sales_df = self.load_df(file_path=file_path)
        self.sales_df["date"] = pd.to_datetime(self.sales_df["date"]).dt.date
        self.sales_df["year"] = self.sales_df.date.dt.year
        self.sales_df = BASE_SCHEMA.validate(self.sales_df)

    def load_prediction_df(
        self,
        file_path: str,
        year: int,
        week_of_year: int,
    ):
        self.prediction_dict[year] = {
            week_of_year: self.load_df(file_path=file_path),
        }


class RegionRepository(object):
    def __init__(self):
        pass

    def select(
        self,
        container: Container,
    ) -> List[Region]:

        data = [Region(**r) for r in records]
        return data


class StoreRepository(object):
    def __init__(self):
        pass
        self.table_name = TABLES.STORES.value

    def select(
        self,
        region: Optional[str] = None,
    ) -> List[Store]:
        query = f"""
SELECT
    {self.table_name}.id,
    {self.table_name}.name,
    {TABLES.REGIONS.value}.name AS region
FROM 
    {self.table_name}
LEFT JOIN
    {TABLES.REGIONS.value}
ON
    {self.table_name}.region_id = {TABLES.REGIONS.value}.id
        """
        parameters = []

        if region is not None:
            where = f"""
WHERE
    {TABLES.REGIONS.value}.name = %s
            """
            parameters.append(region)
            query += where

        query += ";"

        records = self.execute_select_query(
            query=query,
            parameters=tuple(parameters),
        )
        data = [Store(**r) for r in records]
        return data


class ItemRepository(object):
    def __init__(self):
        pass
        self.table_name = TABLES.ITEMS.value

    def select(self) -> List[Item]:
        query = f"""
SELECT
    id,
    name
FROM 
    {self.table_name}
;
        """

        records = self.execute_select_query(query=query)
        data = [Item(**r) for r in records]
        return data


class ItemSalesRepository(object):
    def __init__(self):
        pass
        self.table_name = TABLES.ITEM_SALES_RECORDS.value

    def select(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        day_of_week: Optional[str] = None,
        item: Optional[str] = None,
        store: Optional[str] = None,
        region: Optional[str] = None,
        limit: int = 1000,
        offset: int = 0,
    ) -> List[ItemSales]:
        query = f"""
SELECT
    {self.table_name}.id,
    {self.table_name}.date,
    {self.table_name}.day_of_week,
    {self.table_name}.week_of_year,
    {TABLES.ITEMS.value}.name AS item,
    {TABLES.ITEM_PRICES.value}.price AS item_price,
    {TABLES.STORES.value}.name as store,
    {TABLES.REGIONS.value}.name as region,
    {self.table_name}.sales,
    {self.table_name}.total_sales_amount
FROM 
    {self.table_name}
LEFT JOIN
    {TABLES.ITEM_PRICES.value}
ON
    {TABLES.ITEM_PRICES.value}.item_id = {TABLES.ITEM_SALES_RECORDS.value}.item_id
AND
    (
        {TABLES.ITEM_PRICES.value}.applied_from <= {TABLES.ITEM_SALES_RECORDS.value}.date
        AND
        {TABLES.ITEM_PRICES.value}.applied_to >= {TABLES.ITEM_SALES_RECORDS.value}.date
    )
LEFT JOIN
    {TABLES.ITEMS.value}
ON
    {self.table_name}.item_id = {TABLES.ITEMS.value}.id
LEFT JOIN
    {TABLES.STORES.value}
ON
    {self.table_name}.store_id = {TABLES.STORES.value}.id
LEFT JOIN
    {TABLES.REGIONS.value}
ON
    {TABLES.STORES.value}.region_id = {TABLES.REGIONS.value}.id
        """

        where = ""
        prefix = "WHERE"
        parameters = []
        if date_from is not None:
            where += f"{prefix} {self.table_name}.date >= %s "
            parameters.append(date_from)
            prefix = "AND"
        if date_to is not None:
            where += f"{prefix} {self.table_name}.date <= %s "
            parameters.append(date_to)
            prefix = "AND"
        if day_of_week is not None:
            where += f"{prefix} {self.table_name}.day_of_week = %s "
            parameters.append(day_of_week)
            prefix = "AND"
        if item is not None:
            where += f"{prefix} {TABLES.ITEMS.value}.name = %s "
            parameters.append(item)
            prefix = "AND"
        if store is not None:
            where += f"{prefix} {TABLES.STORES.value}.name = %s "
            parameters.append(store)
            prefix = "AND"
        if region is not None:
            where += f"{prefix} {TABLES.REGIONS.value}.name = %s "
            parameters.append(region)
        query += where
        query += f"""
LIMIT 
    {limit}
OFFSET
    {offset}
        """

        records = self.execute_select_query(
            query=query,
            parameters=tuple(parameters),
        )
        data = [ItemSales(**r) for r in records]
        return data


class ItemWeeklySalesPredictionsRepository(object):
    def __init__(self):
        pass
        self.table_name = TABLES.ITEM_WEEKLY_SALES_PREDICTIONS.value

    def select(
        self,
        item: Optional[str] = None,
        store: Optional[str] = None,
        region: Optional[str] = None,
        year: Optional[int] = None,
        week_of_year: Optional[int] = None,
        version: int = 0,
        limit: int = 1000,
        offset: int = 0,
    ) -> List[ItemWeeklySalesPredictions]:
        query = f"""
SELECT
    {self.table_name}.id,
    {TABLES.STORES.value}.name as store,
    {TABLES.REGIONS.value}.name as region,
    {TABLES.ITEMS.value}.name AS item,
    {self.table_name}.year,
    {self.table_name}.week_of_year,
    {self.table_name}.prediction,
    {self.table_name}.predicted_at,
    {self.table_name}.version
FROM 
    {self.table_name}
LEFT JOIN
    {TABLES.ITEMS.value}
ON
    {self.table_name}.item_id = {TABLES.ITEMS.value}.id
LEFT JOIN
    {TABLES.STORES.value}
ON
    {self.table_name}.store_id = {TABLES.STORES.value}.id
LEFT JOIN
    {TABLES.REGIONS.value}
ON
    {TABLES.STORES.value}.region_id = {TABLES.REGIONS.value}.id
        """

        where = ""
        prefix = "WHERE"
        parameters = []
        if item is not None:
            where += f"{prefix} {TABLES.ITEMS.value}.name = %s "
            parameters.append(item)
            prefix = "AND"
        if store is not None:
            where += f"{prefix} {TABLES.STORES.value}.name = %s "
            parameters.append(store)
            prefix = "AND"
        if region is not None:
            where += f"{prefix} {TABLES.REGIONS.value}.name = %s "
            parameters.append(region)
            prefix = "AND"
        if year is not None:
            where += f"{prefix} {self.table_name}.year = %s "
            parameters.append(year)
            prefix = "AND"
        if week_of_year is not None:
            where += f"{prefix} {self.table_name}.week_of_year = %s "
            parameters.append(week_of_year)
            prefix = "AND"
        if version is not None:
            where += f"{prefix} {self.table_name}.version = %s "
            parameters.append(version)
            prefix = "AND"
        query += where
        query += f"""
LIMIT 
    {limit}
OFFSET
    {offset}
        """

        records = self.execute_select_query(
            query=query,
            parameters=tuple(parameters),
        )
        data = [ItemWeeklySalesPredictions(**r) for r in records]
        return data
