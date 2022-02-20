from datetime import datetime
from logging import getLogger
from typing import List, Optional

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
    user_id: str
    name: str
    description: str
    photo_url: str
    deactivated: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class AnimalRepository(BaseRepository):
    def __init__(
        self,
        db_client: AbstractDBClient,
    ):
        super().__init__(db_client=db_client)
        self.animal_table = TABLES.ANIMAL.value

    def select(
        self,
        animal_query: Optional[AnimalQuery] = None,
        limit: int = 200,
        offset: int = 0,
    ) -> List[Animal]:
        parameters = []
        query = f"""
SELECT
    {self.animal_table}.id,
    {self.animal_table}.animal_category_id,
    {self.animal_table}.animal_subcategory_id,
    {self.animal_table}.user_id,
    {self.animal_table}.name,
    {self.animal_table}.description,
    {self.animal_table}.photo_url,
    {self.animal_table}.deactivated,
    {self.animal_table}.created_at,
    {self.animal_table}.updated_at
FROM 
    {self.animal_table}
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
        animal_query: Optional[AnimalQuery] = None,
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
            if len(r) > 0:
                records.extend(r)
            else:
                break
            offset += limit
        return records
