import json
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, List

from src.infrastructure.cache_client import AbstractCacheClient

logger = getLogger(__name__)


class AbstractFeatureCacheRepository(ABC):
    def __init__(
        self,
        cache: AbstractCacheClient,
    ):
        self.cache = cache

    @abstractmethod
    def get_features_by_keys(
        self,
        keys: List[str],
    ) -> Dict[str, Dict[str, List[float]]]:
        raise NotImplementedError


class FeatureCacheRepository(AbstractFeatureCacheRepository):
    def __init__(
        self,
        cache: AbstractCacheClient,
    ):
        super().__init__(cache=cache)

    def get_features_by_keys(
        self,
        keys: List[str],
    ) -> Dict[str, Dict[str, List[float]]]:
        features = {}
        for key in keys:
            feature = self.cache.get(key=key)
            if feature is not None:
                features[key] = json.loads(str(feature))
        return features
