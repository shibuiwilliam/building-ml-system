from datetime import date
from typing import List, Optional

from src.constants import TABLES
from src.infrastructure.database import AbstractDBClient
from src.middleware.logger import configure_logger
from src.model.item_sales_model import ItemSales
from src.repository.abstract_repository import AbstractQuery, AbstractRepository, BaseRepository

logger = configure_logger(__name__)


class ItemSalesQuery(AbstractQuery):
    ids: Optional[List[str]]
    date_from: Optional[date]
    date_to: Optional[date]
    store_ids: Optional[List[str]]
    item_ids: Optional[List[str]]
    sales_below: Optional[int]
    sales_over: Optional[int]


class ItemSalesRepository(AbstractRepository, BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        AbstractRepository.__init__(self)
        BaseRepository.__init__(self, db_client=db_client)
        self.table_name = TABLES.ITEM_SALES_RECORDS.value
        self.columns = [
            f"{self.table_name}.id",
            f"{self.table_name}.date",
            f"{self.table_name}.day_of_week",
            f"{self.table_name}.week_of_year",
            f"{self.table_name}.store_id",
            f"{self.table_name}.item_id",
            f"{self.table_name}.sales",
            f"{self.table_name}.total_sales_amount",
            f"{self.table_name}.created_at",
            f"{self.table_name}.updated_at",
        ]

    def insert(
        self,
        record: ItemSales,
    ):
        d = record.dict()
        _columns = [c for c, p in d.items() if p is not None]
        columns = ",".join(_columns)
        values = ",".join(["%s" for _ in _columns])
        parameters = tuple([p for p in d.values() if p is not None])
        query = f"""
INSERT INTO
    {self.table_name}
    ({columns})
VALUES
    ({values})
ON CONFLICT
    (id)
DO NOTHING
;
        """
        self.execute_insert_or_update_query(
            query=query,
            parameters=parameters,
        )

    def bulk_insert(
        self,
        records: List[ItemSales],
    ):
        _columns = [
            "id",
            "date",
            "day_of_week",
            "week_of_year",
            "store_id",
            "item_id",
            "sales",
            "total_sales_amount",
        ]
        columns = ",".join(_columns)
        query = f"""
INSERT INTO
    {self.table_name}
    ({columns})
VALUES
    %s
;
        """

        parameters = []
        for d in records:
            values = tuple(
                [
                    d.id,
                    d.date,
                    d.day_of_week,
                    d.week_of_year,
                    d.store_id,
                    d.item_id,
                    d.sales,
                    d.total_sales_amount,
                ]
            )
            parameters.append(values)
        self.execute_bulk_insert_or_update_query(
            query=query,
            parameters=parameters,
        )

    def select(
        self,
        condition: Optional[ItemSalesQuery] = None,
    ) -> List[ItemSales]:
        columns = ",".join(self.columns)
        parameters = []
        query = f"""
SELECT
    {columns}
FROM
    {self.table_name}
        """

        if condition is not None:
            where = ""
            prefix = "WHERE"
            if condition.ids is not None and len(condition.ids) > 0:
                _params = ",".join(["%s" for _ in condition.ids])
                where += f"{prefix} {self.table_name}.id IN {_params}"
                parameters.extend(condition.ids)
                prefix = "AND"
            if condition.date_from is not None:
                where += f"{prefix} {self.table_name}.date >= {condition.date_from}"
                parameters.append(condition.date_from)
                prefix = "AND"
            if condition.date_to is not None:
                where += f"{prefix} {self.table_name}.date <= {condition.date_to}"
                parameters.append(condition.date_to)
                prefix = "AND"
            if condition.store_ids is not None and len(condition.store_ids) > 0:
                _params = ",".join(["%s" for _ in condition.store_ids])
                where += f"{prefix} {self.table_name}.name IN {_params}"
                parameters.extend(condition.store_ids)
                prefix = "AND"
            if condition.item_ids is not None and len(condition.item_ids) > 0:
                _params = ",".join(["%s" for _ in condition.item_ids])
                where += f"{prefix} {self.table_name}.name IN {_params}"
                parameters.extend(condition.item_ids)
                prefix = "AND"
            if condition.sales_below is not None:
                where += f"{prefix} {self.table_name}.sales >= {condition.sales_below}"
                parameters.append(condition.sales_below)
                prefix = "AND"
            if condition.sales_over is not None:
                where += f"{prefix} {self.table_name}.sales <= {condition.sales_over}"
                parameters.append(condition.sales_over)

            query += where
        query += ";"
        records = self.execute_select_query(
            query=query,
            parameters=tuple(parameters),
        )
        data = [ItemSales(**r) for r in records]
        return data

    def select_latest(self) -> List[ItemSales]:
        columns = ",".join(self.columns)
        query = f"""
SELECT
    {columns}
FROM
    {self.table_name}
WHERE
    {self.table_name}.date = (
        SELECT
            MAX({self.table_name}.date)
        FROM
            {self.table_name}
    )
LIMIT
    1
;
        """

        records = self.execute_select_query(
            query=query,
            parameters=None,
        )
        data = [ItemSales(**r) for r in records]
        return data
