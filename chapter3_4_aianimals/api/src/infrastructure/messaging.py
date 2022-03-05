from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict

logger = getLogger(__name__)


class AbstractMessaging(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def init_channel(self):
        raise NotImplementedError

    @abstractmethod
    def create_queue(
        self,
        queue_name: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @abstractmethod
    def publish(
        self,
        queue_name: str,
        body: Dict,
    ):
        raise NotImplementedError
