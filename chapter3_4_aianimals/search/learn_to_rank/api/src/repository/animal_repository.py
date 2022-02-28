from logging import getLogger
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Extra
from src.infrastructure.db_client import AbstractDBClient
from src.repository.base_repository import TABLES, BaseRepository

logger = getLogger(__name__)


class AnimalQuery(BaseModel):
    ids: List[str]

    class Config:
        extra = Extra.forbid


class Animal(BaseModel):
    id: str
    animal_category_id: int
    animal_subcategory_id: int
    likes: int = 0
    name_vector: Union[Dict, List]
    description_vector: Union[Dict, List]

    class Config:
        extra = Extra.forbid


class AnimalRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.animal_table = TABLES.ANIMAL.value
        self.like_table = TABLES.LIKE.value

    def select(
        self,
        animal_query: AnimalQuery,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Animal]:
        parameters = []
        subquery = f"""
            SELECT
                COUNT({self.like_table}.animal_id) AS likes,
                {self.like_table}.animal_id
            FROM
                {self.like_table}
        """
        if animal_query is not None and len(animal_query.ids) > 0:
            parameters.extend(animal_query.ids)
            ids = ",".join(["%s" for _ in animal_query.ids])
            subquery += f"""
            WHERE
                {self.like_table}.animal_id IN ({ids})
            """
        subquery += f"""
            GROUP BY
                {self.like_table}.animal_id
        """

        query = f"""
            SELECT
                {self.animal_table}.id,
                {self.animal_table}.animal_category_id,
                {self.animal_table}.animal_subcategory_id,
                (CASE WHEN likes.likes is NULL THEN 0 ELSE likes.likes END) AS likes,
            FROM 
                {self.animal_table}
            LEFT JOIN
                (
                    {subquery}
                ) likes
            ON
                likes.animal_id = {self.animal_table}.id
        """

        if animal_query is not None and len(animal_query.ids) > 0:
            parameters.extend(animal_query.ids)
            ids = ",".join(["%s" for _ in animal_query.ids])
            query += f"""
            WHERE
                {self.animal_table}.id IN ({ids})
            """

        query += f"""
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
        data = [Animal(**r) for r in records]
        return data

    def select_all(
        self,
        animal_query: AnimalQuery,
    ) -> List[Animal]:
        limit = 200
        offset = 0
        records = []
        while True:
            r = self.select(
                animal_query=animal_query,
                limit=limit,
                offset=offset,
            )
            if len(r) == len(animal_query.ids):
                records.extend(r)
                break
            if len(r) > 0:
                records.extend(r)
            else:
                break
            offset += limit
        return records
