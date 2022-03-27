import os
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, List, Optional, Union

from elasticsearch import Elasticsearch
from src.entities.animal import AnimalSearchQuery, AnimalSearchResult, AnimalSearchResults, AnimalSearchSortKey
from src.middleware.strings import hiragana_to_katakana, katakana_to_hiragana

logger = getLogger(__name__)


class AbstractSearch(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def search(
        self,
        index: str,
        query: AnimalSearchQuery,
        from_: int = 0,
        size: int = 100,
    ) -> AnimalSearchResults:
        raise NotImplementedError


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

    def __make_sort(
        self,
        key: Optional[AnimalSearchSortKey],
    ) -> List[Union[str, Dict]]:
        sort: List[Union[str, Dict]] = []
        if key is not None and key:
            if key == AnimalSearchSortKey.RANDOM:
                sort.append(
                    {
                        "_script": {
                            "script": "Math.random() * 200000",
                            "type": "number",
                            "order": "asc",
                        }
                    }
                )
            elif key == AnimalSearchSortKey.SCORE or key == AnimalSearchSortKey.LEARN_TO_RANK:
                sort.append("_score")
            else:
                sort.append(
                    {
                        key.value: {
                            "order": "desc",
                        }
                    }
                )
        return sort

    def __augment_query(
        self,
        vocab: str,
    ) -> List[str]:
        vocabs = [vocab]
        if vocab in ["ねこ", "猫", "ネコ"]:
            vocabs.extend(["ねこ", "猫", "ネコ"])
        if vocab in ["いぬ", "犬", "イヌ"]:
            vocabs.extend(["いぬ", "犬", "イヌ"])
        if vocab in ["かわいい", "可愛い", "カワイイ"]:
            vocabs.extend(["かわいい", "可愛い", "カワイイ"])
        katakana = hiragana_to_katakana(hiragana=vocab)
        vocabs.append(katakana)
        hiragana = katakana_to_hiragana(katakana=vocab)
        vocabs.append(hiragana)

        return list(set(vocabs))

    def search(
        self,
        index: str,
        query: AnimalSearchQuery,
        from_: int = 0,
        size: int = 100,
    ) -> AnimalSearchResults:
        q: Dict[str, Dict] = {"bool": {}}
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
            phrases = []
            for p in query.phrases:
                phrase = self.__augment_query(vocab=p)
                phrases.extend(phrase)
            query_phrase = " ".join(phrases)
            q["bool"]["should"] = [
                {
                    "match": {"name": query_phrase},
                },
                {
                    "match": {"description": query_phrase},
                },
            ]
        if len(q["bool"]) == 0:
            q = {"match_all": {}}
        sort = self.__make_sort(key=query.sort_by if query is not None else None)
        searched = self.es_client.search(
            index=index,
            query=q,
            sort=sort,
            from_=from_,
            size=size,
        )
        logger.info(f"CCCCCCCCCCCCCCCCCCCc: {searched}")
        if searched["hits"]["total"]["value"] == 0:
            return AnimalSearchResults(
                hits=0,
                max_score=0,
                results=[],
                offset=0,
            )
        results = AnimalSearchResults(
            hits=searched["hits"]["total"]["value"],
            max_score=searched["hits"]["max_score"],
            results=[],
            offset=from_ + min(size, searched["hits"]["total"]["value"]),
        )
        logger.info(f"DDDDDDDDDDDDDDDDDDDDDDDDD: {results}")
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
                    like=r["_source"]["like"],
                    created_at=r["_source"]["created_at"],
                ),
            )
        logger.info(f"EEEEEEEEEEEEEEEEEEEEEEEE: {results}")
        return results
