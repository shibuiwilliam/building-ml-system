from abc import ABC, abstractmethod

from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractMessaging(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def callback(
        ch,
        method,
        properties,
        body,
    ):
        raise NotImplementedError

    @abstractmethod
    def consume(self):
        raise NotImplementedError
