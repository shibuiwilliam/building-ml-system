from src.configurations import Configurations
from src.infrastructure.cache_client import AbstractCacheClient, RedisClient
from src.infrastructure.db_client import AbstractDBClient, DBClient
from src.repository.animal_repository import AnimalRepository
from src.service.predictor import AbstractPredictor, SimilarImageSearchPredictor
from src.usecase.search_similar_image_usecase import AbstractSearchSimilarImageUsecase, SearchSimilarImageUsecase


class Container(object):
    def __init__(
        self,
        db_client: AbstractDBClient,
        cache_client: AbstractCacheClient,
        predictor: AbstractPredictor,
    ):
        self.db_client = db_client
        self.cache_client = cache_client
        self.predictor = predictor

        self.animal_repository: AnimalRepository = AnimalRepository(db_client=self.db_client)
        self.search_similar_image_usecase: AbstractSearchSimilarImageUsecase = SearchSimilarImageUsecase(
            animal_repository=self.animal_repository,
            cache_client=self.cache_client,
            predictor=self.predictor,
            threshold=Configurations.threshold,
        )


container = Container(
    db_client=DBClient(),
    cache_client=RedisClient(),
    predictor=SimilarImageSearchPredictor(
        url=Configurations.predictor_url,
        height=Configurations.predictor_height,
        width=Configurations.predictor_width,
    ),
)
