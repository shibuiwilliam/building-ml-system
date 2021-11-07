from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
from psycopg2.extras import DictCursor
from src.dataset.schema import BASE_SCHEMA, TABLES, ItemSales
from src.middleware.db_client import AbstractDBClient
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class DATA_SOURCE(Enum):
    LOCAL = "local"
    DB = "db"

    @staticmethod
    def list_values() -> List[str]:
        return [v.value for v in DATA_SOURCE.__members__.values()]

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in DATA_SOURCE.__members__.values()]

    @staticmethod
    def value_to_enum(value: str):
        for v in DATA_SOURCE.__members__.values():
            if value == v.value:
                return v
        raise ValueError


def load_df_from_csv(file_path: str) -> pd.DataFrame:
    logger.info(f"load dataframe from {file_path}")
    df = pd.read_csv(file_path)
    df = BASE_SCHEMA.validate(df)
    return df


def save_df_to_csv(
    df: pd.DataFrame,
    file_path: str,
):
    logger.info(f"save dataframe to {file_path}")
    df.to_csv(file_path, index=False)


class DBDataManager(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client

    def load_df_from_db(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        day_of_week: Optional[str] = None,
        item: Optional[str] = None,
        store: Optional[str] = None,
        region: Optional[str] = None,
    ) -> pd.DataFrame:
        item_sales: List[ItemSales] = []
        limit = 10000
        offset = 0
        while True:
            records = self.select_item_sales(
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

        df = pd.DataFrame([d.dict() for d in item_sales])
        df = BASE_SCHEMA.validate(df)
        return df

    def execute_select_query(
        self,
        query: str,
        parameters: Optional[Tuple] = None,
    ) -> List[Dict[str, Any]]:
        logger.info(f"select query: {query}, parameters: {parameters}")
        with self.db_client.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, parameters)
                rows = cursor.fetchall()
        return rows

    def select_item_sales(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        day_of_week: Optional[str] = None,
        item: Optional[str] = None,
        store: Optional[str] = None,
        region: Optional[str] = None,
        limit: int = 10000,
        offset: int = 0,
    ) -> List[ItemSales]:
        query = f"""
SELECT
    {TABLES.ITEM_SALES_RECORDS.value}.date,
    {TABLES.ITEM_SALES_RECORDS.value}.day_of_week,
    {TABLES.ITEMS.value}.name AS item,
    {TABLES.ITEM_PRICES.value}.price AS item_price,
    {TABLES.STORES.value}.name as store,
    {TABLES.ITEM_SALES_RECORDS.value}.sales,
    {TABLES.ITEM_SALES_RECORDS.value}.total_sales_amount
FROM 
    {TABLES.ITEM_SALES_RECORDS.value}
LEFT JOIN
    {TABLES.ITEMS.value}
ON
    {TABLES.ITEM_SALES_RECORDS.value}.item_id = {TABLES.ITEMS.value}.id
LEFT JOIN
    {TABLES.ITEM_PRICES.value}
ON
    {TABLES.ITEM_SALES_RECORDS.value}.item_price_id = {TABLES.ITEM_PRICES.value}.id
LEFT JOIN
    {TABLES.STORES.value}
ON
    {TABLES.ITEM_SALES_RECORDS.value}.store_id = {TABLES.STORES.value}.id
LEFT JOIN
    {TABLES.REGIONS.value}
ON
    {TABLES.STORES.value}.region_id = {TABLES.REGIONS.value}.id
"""

        where = ""
        prefix = "WHERE"
        parameters: List[Union[date, str, int]] = []
        if date_from is not None:
            where += f"{prefix} {TABLES.ITEM_SALES_RECORDS.value}.date >= %s "
            parameters.append(date_from)
            prefix = "AND"
        if date_to is not None:
            where += f"{prefix} {TABLES.ITEM_SALES_RECORDS.value}.date <= %s "
            parameters.append(date_to)
            prefix = "AND"
        if day_of_week is not None:
            where += f"{prefix} {TABLES.ITEM_SALES_RECORDS.value}.day_of_week = %s "
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
