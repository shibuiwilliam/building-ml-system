from calendar import c

from src.configurations import Configurations
from src.infrastructure.cache_client import AbstractCacheClient, RedisClient
from src.infrastructure.db_client import AbstractDBClient, DBClient
from src.repository.like_repository import LikeRepository
from src.repository.feature_cache_repository import AbstractFeatureCacheRepository, FeatureCacheRepository
from src.service.learn_to_rank_predict_service import AbstractLearnToRankPredictService, LearnToRankPredictService
from src.usecase.reorder_usecase import AbstractReorderUsecase, ReorderUsecase


class Container(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
        cache_client: AbstractCacheClient,
        preprocess_likes_scaler_file_path: str,
        preprocess_query_animal_category_id_encoder_file_path: str,
        preprocess_query_animal_subcategory_id_encoder_file_path: str,
        preprocess_query_phrase_encoder_file_path: str,
        predictor_file_path: str,
    ):
        self.db_client = db_client
        self.cache_client = cache_client
        self.preprocess_likes_scaler_file_path = preprocess_likes_scaler_file_path
        self.preprocess_query_animal_category_id_encoder_file_path = (
            preprocess_query_animal_category_id_encoder_file_path
        )
        self.preprocess_query_animal_subcategory_id_encoder_file_path = (
            preprocess_query_animal_subcategory_id_encoder_file_path
        )
        self.preprocess_query_phrase_encoder_file_path = preprocess_query_phrase_encoder_file_path
        self.predictor_file_path = predictor_file_path

        self.learn_to_rank_predictor_service: AbstractLearnToRankPredictService = LearnToRankPredictService(
            preprocess_likes_scaler_file_path=self.preprocess_likes_scaler_file_path,
            preprocess_query_animal_category_id_encoder_file_path=self.preprocess_query_animal_category_id_encoder_file_path,
            preprocess_query_animal_subcategory_id_encoder_file_path=self.preprocess_query_animal_subcategory_id_encoder_file_path,
            preprocess_query_phrase_encoder_file_path=self.preprocess_query_phrase_encoder_file_path,
            predictor_file_path=self.predictor_file_path,
        )

        self.like_repository: LikeRepository = LikeRepository(db_client=self.db_client)
        self.feature_cache_repository: AbstractFeatureCacheRepository = FeatureCacheRepository(cache=self.cache_client)
        self.reorder_usecase: AbstractReorderUsecase = ReorderUsecase(
            like_repository=self.like_repository,
            feature_cache_repository=self.feature_cache_repository,
            db_client=self.db_client,
            cache_client=self.cache_client,
            learn_to_rank_predict_service=self.learn_to_rank_predictor_service,
        )


container = Container(
    db_client=DBClient(),
    cache_client=RedisClient(),
    preprocess_likes_scaler_file_path=Configurations.preprocess_likes_scaler_file_path,
    preprocess_query_animal_category_id_encoder_file_path=Configurations.preprocess_query_animal_category_id_encoder_file_path,
    preprocess_query_animal_subcategory_id_encoder_file_path=Configurations.preprocess_query_animal_subcategory_id_encoder_file_path,
    preprocess_query_phrase_encoder_file_path=Configurations.preprocess_query_phrase_encoder_file_path,
    predictor_file_path=Configurations.predictor_file_path,
)
