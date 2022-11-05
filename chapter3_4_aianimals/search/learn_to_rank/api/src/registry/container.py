from abc import ABC

from src.infrastructure.cache_client import AbstractCacheClient
from src.infrastructure.db_client import AbstractDBClient
from src.repository.feature_cache_repository import AbstractFeatureCacheRepository, FeatureCacheRepository
from src.repository.like_repository import LikeRepository
from src.service.learn_to_rank_service import AbstractLearnToRankService
from src.usecase.reorder_usecase import AbstractReorderUsecase, ReorderUsecase


class AbstractContainer(ABC):
    def __init__(self):
        self.reorder_usecase: AbstractReorderUsecase = None


class Container(AbstractContainer):
    def __init__(
        self,
        db_client: AbstractDBClient,
        cache_client: AbstractCacheClient,
        learn_to_rank_service: AbstractLearnToRankService,
    ):
        super().__init__()

        self.db_client = db_client
        self.cache_client = cache_client
        self.learn_to_rank_service = learn_to_rank_service

        self.like_repository: LikeRepository = LikeRepository(db_client=self.db_client)
        self.feature_cache_repository: AbstractFeatureCacheRepository = FeatureCacheRepository(cache=self.cache_client)
        self.reorder_usecase: AbstractReorderUsecase = ReorderUsecase(
            like_repository=self.like_repository,
            feature_cache_repository=self.feature_cache_repository,
            db_client=self.db_client,
            cache_client=self.cache_client,
            learn_to_rank_service=self.learn_to_rank_service,
        )


class EmptyContainer(AbstractContainer):
    def __init__(self):
        super().__init__()
