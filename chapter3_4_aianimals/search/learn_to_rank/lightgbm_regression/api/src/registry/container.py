from src.configurations import Configurations
from src.infrastructure.cache_client import AbstractCacheClient, RedisClient
from src.infrastructure.db_client import AbstractDBClient, DBClient
from src.infrastructure.predictor_client import AbstractPredictor, Predictor
from src.repository.animal_repository import AnimalRepository
from src.service.learn_to_rank_predict_service import AbstractLearnToRankPredictService, LearnToRankPredictService
from src.usecase.reorder_usecase import AbstractReorderUsecase, ReorderUsecase


class Container(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
        cache_client: AbstractCacheClient,
        predictor: AbstractPredictor,
        preprocess_file_path: str,
    ):
        self.db_client = db_client
        self.cache_client = cache_client
        self.predictor = predictor
        self.preprocess_file_path = preprocess_file_path

        self.learn_to_rank_predictor_service: AbstractLearnToRankPredictService = LearnToRankPredictService(
            predictor=self.predictor,
            preprocess_file_path=self.preprocess_file_path,
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
    predictor=Predictor(
        endpoint=Configurations.endpoint,
        input_name=Configurations.input_name,
        output_name=Configurations.output_name,
        batch_size=Configurations.batch_size,
        feature_size=Configurations.feature_size,
        retries=Configurations.retries,
        timeout=Configurations.timeout,
    ),
    preprocess_file_path=Configurations.preprocess_file_path,
)
