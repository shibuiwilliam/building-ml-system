from typing import List, Optional

from src.constants import TABLES
from src.infrastructure.database import AbstractDBClient
from src.middleware.logger import configure_logger
from src.model.store_model import Store
from src.repository.abstract_repository import AbstractQuery, AbstractRepository, BaseRepository

logger = configure_logger(__name__)


class StoreQuery(AbstractQuery):
    ids: Optional[List[str]]
    names: Optional[List[str]]
    region_ids: Optional[List[str]]


class StoreRepository(AbstractRepository, BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        AbstractRepository.__init__(self)
        BaseRepository.__init__(self, db_client=db_client)
        self.table_name = TABLES.STORES.value
        self.columns = [
            f"{self.table_name}.id",
            f"{self.table_name}.name",
            f"{self.table_name}.region_id",
        ]

    def insert(
        self,
        record: Store,
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

    def select(
        self,
        condition: Optional[StoreQuery] = None,
    ) -> List[Store]:
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
            if condition.names is not None and len(condition.names) > 0:
                _params = ",".join(["%s" for _ in condition.names])
                where += f"{prefix} {self.table_name}.name IN {_params}"
                parameters.extend(condition.names)
                prefix = "AND"
            if condition.region_ids is not None and len(condition.region_ids) > 0:
                _params = ",".join(["%s" for _ in condition.region_ids])
                where += f"{prefix} {self.table_name}.name IN {_params}"
                parameters.extend(condition.region_ids)
            query += where
        query += ";"
        records = self.execute_select_query(
            query=query,
            parameters=tuple(parameters),
        )
        data = [Store(**r) for r in records]
        return data
