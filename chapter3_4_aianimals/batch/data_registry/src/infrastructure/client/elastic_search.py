import os
from typing import Dict, Union

from elasticsearch import Elasticsearch
from src.infrastructure.search import AbstractSearch
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class ElasticsearchClient(AbstractSearch):
    def __init__(self):
        super().__init__()
        self.__es_host = os.getenv("ES_HOST", "http://es:9200")
        self.__es_verify_certs = bool(int(os.getenv("ES_VERIFY_CERTS", 0)))
        self.__es_user = os.getenv("ES_USER", None)
        self.__es_password = os.getenv("ES_PASSWORD", None)
        self.__basic_auth = (
            (self.__es_user, self.__es_password)
            if self.__es_user is not None and self.__es_password is not None
            else None
        )
        self.es_client = Elasticsearch(
            hosts=[self.__es_host],
            verify_certs=self.__es_verify_certs,
            basic_auth=self.__basic_auth,
        )

    def create_index(
        self,
        index: str,
        body: Dict,
    ):
        logger.info(f"register index {index} with body {body}")
        self.es_client.indices.create(
            index=index,
            body=body,
        )
        logger.info(f"done register index {index} with body {body}")

    def get_index(
        self,
        index: str,
    ) -> Dict:
        return self.es_client.indices.get_mapping(index=index)

    def index_exists(
        self,
        index: str,
    ) -> bool:
        indices = self.es_client.cat.indices(index="*", h="index").splitlines()
        logger.info(f"indices: {indices}")
        return index in indices

    def create_document(
        self,
        index: str,
        id: Union[str, int],
        body: Dict,
    ):
        logger.info(f"register document in index {index} with id {id} and body {body}")
        self.es_client.create(
            index=index,
            id=id,
            body=body,
        )

    def update_document(
        self,
        index: str,
        id: Union[str, int],
        doc: Dict,
    ):
        logger.info(f"update document in index {index} with id {id} and body {doc}")
        self.es_client.update(
            index=index,
            id=id,
            doc=doc,
            refresh=True,
        )

    def is_document_exist(
        self,
        index: str,
        id: Union[str, int],
    ) -> bool:
        exists = self.es_client.exists(
            index=index,
            id=id,
        )
        logger.info(f"exists: {exists}")
        return exists
