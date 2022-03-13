import os
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Optional

import redis

logger = getLogger(__name__)


class AbstractCacheClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def set(
        self,
        key: str,
        value: str,
        expire_second: int = 60 * 60 * 6,
    ):
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        key: str,
    ) -> Optional[str]:
        raise NotImplementedError


class RedisClient(AbstractCacheClient):
    def __init__(self):
        super().__init__()
        self.__redis_host = os.environ["REDIS_HOST"]
        self.__redis_port = os.getenv("REDIS_PORT", 6379)
        self.__redis_db = int(os.getenv("REDIS_DB", 0))

        self.redis_client = redis.Redis(
            host=self.__redis_host,
            port=self.__redis_port,
            db=self.__redis_db,
            decode_responses=True,
        )

    def set(
        self,
        key: str,
        value: str,
        expire_second: int = 60 * 60 * 6,
    ):
        self.redis_client.set(
            name=key,
            value=value,
            ex=expire_second,
        )

    def get(
        self,
        key: str,
    ) -> Optional[str]:
        value = self.redis_client.get(key)
        return value
