from abc import ABC, abstractmethod
from typing import Optional, Tuple

from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractQueue(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def enqueue(
        self,
        queue_name: str,
        key: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def dequeue(
        self,
        queue_name: str,
    ) -> Optional[Tuple[int, str, float, bool]]:
        raise NotImplementedError
