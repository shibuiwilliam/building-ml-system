from abc import ABC, abstractmethod

from sqlalchemy.engine import Engine
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class AbstractDatabase(ABC):
    def __init__(self):
        self.engine: Engine

    @abstractmethod
    def get_session(self):
        raise NotImplementedError
