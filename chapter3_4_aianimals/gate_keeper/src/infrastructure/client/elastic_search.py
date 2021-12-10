import os
from typing import Dict, Tuple

from elasticsearch import Elasticsearch as ES
from src.infrastructure.search import AbstractSearch


class Elasticsearch(AbstractSearch):
    def __init__(self):
        super().__init__()
        self.__es_host = os.getenv("ES_HOST", "es")
        self.__es_schema = os.getenv("ES_SCHEMA", "http")
        self.__es_port = int(os.getenv("ES_PORT", 9200))
        self.es_client = ES(
            [self.__es_host],
            scheme=self.__es_schema,
            port=self.__es_port,
        )

    def create_index(
        self,
        index: str,
        body: Dict,
    ):
        self.es_client.create(
            index=index,
            body=body,
        )

    def get_index(
        self,
        index: str,
    ) -> Dict:
        return self.es_client.indices.get_mapping(index=index)

    def create_document(
        self,
        index: str,
        id: Tuple[str, int],
        body: Dict,
    ):
        self.es_client.create(
            index=index,
            id=id,
            body=body,
        )
