from datetime import date
from typing import Any, Dict, List, Optional, Tuple

from constants import TABLES
from db_client import AbstractDBClient
from logger import configure_logger
from psycopg2.extras import DictCursor
from pydantic import BaseModel, Extra

logger = configure_logger(__name__)


class Region(BaseModel):
    id: str
    name: str

    class Config:
        extra = Extra.forbid


class Store(BaseModel):
    id: str
    name: str
    region: str

    class Config:
        extra = Extra.forbid


class Item(BaseModel):
    id: str
    name: str

    class Config:
        extra = Extra.forbid


class ItemSales(BaseModel):
    id: str
    date: date
    day_of_week: str
    store: str
    region: str
    item: str
    price: int
    sales: int
    total_sales_amount: int

    class Config:
        extra = Extra.forbid


class BaseRepository(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        self.db_client = db_client
        self.table_name: str = ""

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


class RegionRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.table_name = TABLES.REGIONS.value

    def select(self) -> List[Region]:
        query = f"""
SELECT
    id,
    name
FROM 
    {self.table_name}
;
        """

        records = self.execute_select_query(query=query)
        data = [Region(**r) for r in records]
        return data


class StoreRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
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


class ItemRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
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


class ItemSalesRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
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
    {TABLES.ITEMS.value}.name AS item,
    {TABLES.ITEM_PRICES.value}.price AS price,
    {TABLES.STORES.value}.name as store,
    {TABLES.REGIONS.value}.name as region,
    {self.table_name}.sales,
    {self.table_name}.total_sales_amount
FROM 
    {self.table_name}
LEFT JOIN
    {TABLES.ITEMS.value}
ON
    {self.table_name}.item_id = {TABLES.ITEMS.value}.id
LEFT JOIN
    {TABLES.ITEM_PRICES.value}
ON
    {self.table_name}.item_price_id = {TABLES.ITEM_PRICES.value}.id
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
