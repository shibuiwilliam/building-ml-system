import os
from logging import getLogger
from typing import Dict, Optional

from elasticsearch import Elasticsearch as ES
from src.entities.animal import AnimalSearchQuery, AnimalSearchResult, AnimalSearchResults
from src.infrastructure.search import AbstractSearch

logger = getLogger(__name__)


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

    def __add_must(
        self,
        q: Dict,
        key: str,
        value: str,
    ) -> Dict:
        if "must" in q["bool"].keys():
            q["bool"]["must"].append(
                {
                    "match": {
                        key: value,
                    }
                }
            )
        else:
            q["bool"]["must"] = [
                {
                    "match": {
                        key: value,
                    }
                }
            ]
        return q

    def search(
        self,
        index: str,
        query: Optional[AnimalSearchQuery] = None,
        from_: int = 0,
        size: int = 20,
    ) -> AnimalSearchResults:
        if query is None:
            q = {"match_all": {}}
        else:
            q = {"bool": {}}
            if query.animal_category_name_en is not None:
                q = self.__add_must(
                    q=q,
                    key="animal_category_name_en",
                    value=query.animal_category_name_en,
                )
            if query.animal_category_name_ja is not None:
                q = self.__add_must(
                    q=q,
                    key="animal_category_name_ja",
                    value=query.animal_category_name_ja,
                )
            if query.animal_subcategory_name_en is not None:
                q = self.__add_must(
                    q=q,
                    key="animal_subcategory_name_en",
                    value=query.animal_subcategory_name_en,
                )
            if query.animal_subcategory_name_ja is not None:
                q = self.__add_must(
                    q=q,
                    key="animal_subcategory_name_ja",
                    value=query.animal_subcategory_name_ja,
                )
            if len(query.phrases) > 0:
                q["bool"]["should"] = [
                    {
                        "match": {"name": " ".join(query.phrases)},
                    },
                    {
                        "match": {"description": " ".join(query.phrases)},
                    },
                ]
        logger.info(f"search query: {q}")
        searched = self.es_client.search(
            index=index,
            query=q,
            from_=from_,
            size=size,
        )
        results = AnimalSearchResults(
            hits=searched["hits"]["total"]["value"],
            max_score=searched["hits"]["max_score"],
            results=[],
        )
        for r in searched["hits"]["hits"]:
            results.results.append(
                AnimalSearchResult(
                    score=r["_score"],
                    id=r["_id"],
                    name=r["_source"]["name"],
                    description=r["_source"]["description"],
                    photo_url=r["_source"]["photo_url"],
                    animal_category_name_en=r["_source"]["animal_category_name_en"],
                    animal_category_name_ja=r["_source"]["animal_category_name_ja"],
                    animal_subcategory_name_en=r["_source"]["animal_subcategory_name_en"],
                    animal_subcategory_name_ja=r["_source"]["animal_subcategory_name_ja"],
                    user_handle_name=r["_source"]["user_handle_name"],
                ),
            )
        return results