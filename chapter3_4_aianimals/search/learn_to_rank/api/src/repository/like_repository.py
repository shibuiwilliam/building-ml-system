from logging import getLogger
from typing import List

from pydantic import BaseModel, Extra
from src.infrastructure.db_client import AbstractDBClient
from src.repository.base_repository import TABLES, BaseRepository

logger = getLogger(__name__)


class LikeQuery(BaseModel):
    animal_ids: List[str]

    class Config:
        extra = Extra.forbid


class Like(BaseModel):
    animal_id: str
    likes: int = 0

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
    ) -> List[Like]:
        query = f"""
            SELECT
                {self.like_table}.animal_id as animal_id,
                COUNT({self.like_table}.animal_id) AS likes
            FROM
                {self.like_table}
            WHERE
                {self.like_table}.animal_id IN ({like_query.animal_ids})
            GROUP BY
                {self.like_table}.animal_id
            LIMIT
                {limit}
            OFFSET
                {offset}
            ;
        """

        records = self.execute_select_query(query=query)
        data = [Like(**r) for r in records]
        return data

    def select_all(
        self,
        like_query: LikeQuery,
    ) -> List[Like]:
        limit = 200
        offset = 0
        records = []
        while True:
            r = self.select(
                like_query=like_query,
                limit=limit,
                offset=offset,
            )
            if len(r) == len(like_query.ids):
                records.extend(r)
                break
            if len(r) > 0:
                records.extend(r)
            else:
                break
            offset += limit
        return records
