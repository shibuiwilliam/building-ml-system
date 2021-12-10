import os
from logging import getLogger
from typing import Optional, Tuple

import redis
from src.infrastructure.queue import AbstractQueue

logger = getLogger(__name__)


class RedisQueue(AbstractQueue):
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

    def enqueue(
        self,
        queue_name: str,
        key: str,
    ):
        try:
            self.redis_client.lpush(queue_name, key)
        except Exception as e:
            logger.error(e)

    def dequeue(
        self,
        queue_name: str,
    ) -> Optional[Tuple[int, str, float, bool]]:
        if self.redis_client.llen(queue_name) > 0:
            return self.redis_client.rpop(queue_name)
        else:
            return None
