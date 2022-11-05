import os
from typing import Optional, Union

import redis
from src.infrastructure.cache import AbstractCache
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class RedisCache(AbstractCache):
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
        value: Union[str, int, float, bool, bytes],
        expire_second: int = 600,
    ):
        self.redis_client.set(
            name=key,
            value=value,
            ex=expire_second,
        )

    def get(
        self,
        key: str,
    ) -> Optional[Union[str, int, float, bool, bytes]]:
        value = self.redis_client.get(key)
        return value
