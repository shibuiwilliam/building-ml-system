from logging import getLogger
from typing import List, Dict

from pydantic import BaseModel, Extra
from src.infrastructure.db_client import AbstractDBClient
from src.repository.base_repository import TABLES, BaseRepository

logger = getLogger(__name__)


class LikeQuery(BaseModel):
    animal_ids: List[str]

    class Config:
        extra = Extra.forbid


class LikeRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.like_table = TABLES.LIKE.value

    def select(
        self,
        like_query: LikeQuery,
        limit: int = 200,
        offset: int = 0,
    ) -> Dict[str, int]:
        parameters = like_query.animal_ids
        ids = ",".join(["%s" for _ in like_query.animal_ids])
        query = f"""
            SELECT
                {self.like_table}.animal_id as animal_id,
                COUNT({self.like_table}.animal_id) AS likes
            FROM
                {self.like_table}
            WHERE
                {self.like_table}.animal_id IN ({ids})
            GROUP BY
                {self.like_table}.animal_id
            LIMIT
                {limit}
            OFFSET
                {offset}
            ;
        """

        records = self.execute_select_query(
            query=query,
            parameters=tuple(parameters),
        )
        data = {r["animal_id"]: int(r["likes"]) for r in records}
        return data

    def select_all(
        self,
        like_query: LikeQuery,
    ) -> Dict[str, int]:
        limit = 200
        offset = 0
        records = {}
        while True:
            data = self.select(
                like_query=like_query,
                limit=limit,
                offset=offset,
            )
            if len(data) == len(like_query.animal_ids):
                for k, v in data.items():
                    records[k] = v
                break
            if len(data) > 0:
                for k, v in data.items():
                    records[k] = v
            else:
                break
            offset += limit
        return records
