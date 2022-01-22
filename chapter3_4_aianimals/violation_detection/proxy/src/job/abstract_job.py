from abc import ABC, abstractmethod

from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractJob(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self):
        raise NotImplementedError
