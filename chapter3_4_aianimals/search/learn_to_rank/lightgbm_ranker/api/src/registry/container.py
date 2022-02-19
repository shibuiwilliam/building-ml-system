from calendar import c

from src.configurations import Configurations
from src.infrastructure.cache_client import AbstractCacheClient, RedisClient
from src.infrastructure.db_client import AbstractDBClient, DBClient
from src.repository.animal_repository import AnimalQuery, AnimalRepository
from src.service.learn_to_rank_predict_service import AbstractLearnToRankPredictService, LearnToRankPredictService
from src.usecase.reorder_usecase import AbstractReorderUsecase, ReorderUsecase


class Container(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
        cache_client: AbstractCacheClient,
        preprocess_file_path: str,
        predictor_file_path: str,
    ):
        self.db_client = db_client
        self.cache_client = cache_client
        self.preprocess_file_path = preprocess_file_path
        self.predictor_file_path = predictor_file_path

        self.learn_to_rank_predictor_service: AbstractLearnToRankPredictService = LearnToRankPredictService(
            preprocess_file_path=self.preprocess_file_path,
            predictor_file_path=self.predictor_file_path,
        )
        self.animal_repository = AnimalRepository(db_client=self.db_client)
        self.reorder_usecase: AbstractReorderUsecase = ReorderUsecase(
            animal_repository=self.animal_repository,
            db_client=self.db_client,
            cache_client=self.cache_client,
            learn_to_rank_predict_service=self.learn_to_rank_predictor_service,
        )


container = Container(
    db_client=DBClient(),
    cache_client=RedisClient(),
    preprocess_file_path=Configurations.preprocess_file_path,
    predictor_file_path=Configurations.predictor_file_path,
)
