from datetime import date
from typing import List, Optional

from src.constants import TABLES
from src.middleware.database import AbstractDBClient
from src.middleware.logger import configure_logger
from src.model.item_price_model import ItemPrice, ItemPriceUpdate
from src.repository.abstract_repository import AbstractQuery, AbstractRepository, BaseRepository

logger = configure_logger(__name__)


class ItemPriceQuery(AbstractQuery):
    ids: Optional[List[str]]
    item_ids: Optional[List[str]]
    applied_at: Optional[date]
    applied_from: Optional[date]
    applied_to: Optional[date]
    applied_from_before: Optional[date]
    applied_from_after: Optional[date]
    applied_to_before: Optional[date]
    applied_to_after: Optional[date]


class ItemPriceRepository(AbstractRepository, BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        AbstractRepository.__init__(self)
        BaseRepository.__init__(self, db_client=db_client)
        self.table_name = TABLES.ITEM_PRICES.value
        self.columns = [
            f"{self.table_name}.id",
            f"{self.table_name}.item_id",
            f"{self.table_name}.price",
            f"{self.table_name}.applied_from",
            f"{self.table_name}.applied_to",
        ]

    def insert(
        self,
        record: ItemPrice,
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

    def update(
        self,
        record: ItemPriceUpdate,
    ):
        set_values = []
        parameters = []
        if record.price is not None:
            set_values.append("price = %s")
            parameters.append(record.price)
        if record.applied_from is not None:
            set_values.append("applied_from = %s")
            parameters.append(record.applied_from)
        if record.applied_to is not None:
            set_values.append("applied_to = %s")
            parameters.append(record.applied_to)
        values = ",".join(set_values)
        parameters.append(record.id)

        query = f"""
UPDATE
    {self.table_name}
SET
    {values}
WHERE
    id = %s
        """
        self.execute_insert_or_update_query(
            query=query,
            parameters=tuple(parameters),
        )

    def select(
        self,
        condition: Optional[ItemPriceQuery] = None,
    ) -> List[ItemPrice]:
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
            if (
                condition.applied_at is not None
                and condition.applied_from is not None
                and condition.applied_from_before is not None
                and condition.applied_from_after is not None
            ):
                raise ValueError(
                    "cannot use applied_at, applied_from, applied_from_before, and applied_from_after simultaneously"
                )
            if (
                condition.applied_at is not None
                and condition.applied_to is not None
                and condition.applied_to_before is not None
                and condition.applied_to_after is not None
            ):
                raise ValueError(
                    "cannot use applied_at, applied_to, applied_to_before, and applied_to_after simultaneously"
                )
            if condition.ids is not None and len(condition.ids) > 0:
                _params = ",".join(["%s" for _ in condition.ids])
                where += f"{prefix} {self.table_name}.id IN {_params}"
                parameters.extend(condition.ids)
                prefix = "AND"
            if condition.item_ids is not None and len(condition.item_ids) > 0:
                _params = ",".join(["%s" for _ in condition.item_ids])
                where += f"{prefix} {self.table_name}.name IN {_params}"
                parameters.extend(condition.item_ids)
                prefix = "AND"
            if condition.applied_at is not None:
                where += f"""
{prefix} (
    {self.table_name}.applied_from <= {condition.applied_at} 
    AND {self.table_name}.applied_to >= {condition.applied_at}
    )
                """
                parameters.append(condition.applied_at)
                parameters.append(condition.applied_at)
                prefix = "AND"
            if condition.applied_from is not None:
                where += f"{prefix} {self.table_name}.applied_from = {condition.applied_from}"
                parameters.append(condition.applied_from)
                prefix = "AND"
            if condition.applied_from_before is not None:
                where += f"{prefix} {self.table_name}.applied_from >= {condition.applied_from_before}"
                parameters.append(condition.applied_from_before)
                prefix = "AND"
            if condition.applied_from_after is not None:
                where += f"{prefix} {self.table_name}.applied_from <= {condition.applied_from_after}"
                parameters.append(condition.applied_from_after)
                prefix = "AND"
            if condition.applied_to is not None:
                where += f"{prefix} {self.table_name}.applied_to = {condition.applied_to}"
                parameters.append(condition.applied_to)
                prefix = "AND"
            if condition.applied_to_before is not None:
                where += f"{prefix} {self.table_name}.applied_to >= {condition.applied_to_before}"
                parameters.append(condition.applied_to_before)
                prefix = "AND"
            if condition.applied_to_after is not None:
                where += f"{prefix} {self.table_name}.applied_to <= {condition.applied_to_after}"
                parameters.append(condition.applied_to_after)

            query += where
        query += ";"
        records = self.execute_select_query(
            query=query,
            parameters=tuple(parameters),
        )
        data = [ItemPrice(**r) for r in records]
        return data
