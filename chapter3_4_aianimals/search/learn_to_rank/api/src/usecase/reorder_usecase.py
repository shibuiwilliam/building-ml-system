from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

import numpy as np
from fastapi import BackgroundTasks
from src.configurations import Configurations
from src.infrastructure.cache_client import AbstractCacheClient
from src.infrastructure.db_client import AbstractDBClient
from src.middleware.string import get_md5_hash
from src.repository.feature_cache_repository import AbstractFeatureCacheRepository
from src.repository.like_repository import LikeQuery, LikeRepository
from src.schema.animal import AnimalRequest, AnimalResponse
from src.service.learn_to_rank_predict_service import AbstractLearnToRankPredictService

logger = getLogger(__name__)


def make_query_id(
    animal_ids: List[str],
    phrases: str,
    animal_category_id: Optional[int],
    animal_subcategory_id: Optional[int],
) -> str:
    animal_idstring = ".".join(sorted(animal_ids))
    query_key = f"{Configurations.model_name}_{phrases}_{animal_category_id}_{animal_subcategory_id}_{animal_idstring}"
    return get_md5_hash(string=query_key)


class AbstractReorderUsecase(ABC):
    def __init__(
        self,
        like_repository: LikeRepository,
        feature_cache_repository: AbstractFeatureCacheRepository,
        db_client: AbstractDBClient,
        cache_client: AbstractCacheClient,
        learn_to_rank_predict_service: AbstractLearnToRankPredictService,
    ):
        self.like_repository = like_repository
        self.feature_cache_repository = feature_cache_repository
        self.db_client = db_client
        self.cache_client = cache_client
        self.learn_to_rank_predict_service = learn_to_rank_predict_service

    @abstractmethod
    def reorder(
        self,
        request: AnimalRequest,
        background_tasks: BackgroundTasks,
    ) -> AnimalResponse:
        raise NotImplementedError


class ReorderUsecase(AbstractReorderUsecase):
    def __init__(
        self,
        like_repository: LikeRepository,
        feature_cache_repository: AbstractFeatureCacheRepository,
        db_client: AbstractDBClient,
        cache_client: AbstractCacheClient,
        learn_to_rank_predict_service: AbstractLearnToRankPredictService,
    ):
        super().__init__(
            like_repository=like_repository,
            feature_cache_repository=feature_cache_repository,
            db_client=db_client,
            cache_client=cache_client,
            learn_to_rank_predict_service=learn_to_rank_predict_service,
        )

    def __set_prediction_cache(
        self,
        query_id: str,
        ordered_animal_ids: List[str],
    ):
        self.cache_client.set(
            key=query_id,
            value=",".join(ordered_animal_ids),
        )

    def reorder(
        self,
        request: AnimalRequest,
        background_tasks: BackgroundTasks,
    ) -> AnimalResponse:
        query_phrases = ".".join(request.query_phrases)
        query_id = make_query_id(
            animal_ids=request.ids,
            phrases=query_phrases,
            animal_category_id=request.query_animal_category_id,
            animal_subcategory_id=request.query_animal_subcategory_id,
        )
        cached_data = self.cache_client.get(key=query_id)
        if cached_data is not None:
            return AnimalResponse(ids=cached_data.split(","))
        _likes = self.like_repository.select_all(like_query=LikeQuery(animal_ids=request.ids))
        likes = [[l.likes] for l in _likes]

        feature_cache_keys = [f"{id}_feature" for id in request.ids]
        features = self.feature_cache_repository.get_features_by_keys(keys=feature_cache_keys)
        transformed_likes = self.learn_to_rank_predict_service.transform_likes_scaler(likes=likes)
        transformed_query_animal_category_id = (
            self.learn_to_rank_predict_service.transform_query_animal_category_id_encoder(
                query_animal_category_id=[[request.query_animal_category_id]]
            )
        )
        transformed_query_animal_subcategory_id = (
            self.learn_to_rank_predict_service.transform_query_animal_subcategory_id_encoder(
                query_animal_subcategory_id=[[request.query_animal_subcategory_id]]
            )
        )
        transformed_query_phrase = self.learn_to_rank_predict_service.transform_query_phrase_encoder(
            query_phrase=[[query_phrases]]
        )

        inputs = [
            [
                *l,
                transformed_query_phrase[0][0],
                transformed_query_animal_category_id[0][0],
                transformed_query_animal_subcategory_id[0][0],
                *f,
            ]
            for l, f in zip(
                transformed_likes,
                features,
            )
        ]
        prediction = self.learn_to_rank_predict_service.predict(
            ids=request.ids,
            input=np.array(inputs),
        )
        ordered_animal_ids = [p[0] for p in prediction]

        background_tasks.add_task(
            self.__set_prediction_cache,
            query_id,
            ordered_animal_ids,
        )
        return AnimalResponse(ids=ordered_animal_ids)
