from logging import getLogger
from typing import Dict, List, Union

from pydantic import BaseModel, Extra
from src.infrastructure.db_client import AbstractDBClient
from src.repository.base_repository import TABLES, BaseRepository

logger = getLogger(__name__)


class AnimalQuery(BaseModel):
    id: str

    class Config:
        extra = Extra.forbid


class Animal(BaseModel):
    id: str
    photo_url: str

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
        animal_query: AnimalQuery,
        limit: int = 1,
        offset: int = 0,
    ) -> List[Animal]:
        parameters = tuple([animal_query.id])

        query = f"""
            SELECT
                {self.animal_table}.id,
                {self.animal_table}.photo_url
            FROM 
                {self.animal_table}
            WHERE
                {self.animal_table}.id = %s
            LIMIT
                {limit}
            OFFSET
                {offset}
            ;
        """

        records = self.execute_select_query(
            query=query,
            parameters=parameters,
        )
        data = [Animal(**r) for r in records]
        return data
