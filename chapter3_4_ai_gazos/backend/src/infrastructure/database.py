from abc import ABC, abstractmethod

from sqlalchemy.engine import Engine


class AbstractDatabase(ABC):
    def __init__(self):
        self.engine: Engine

    @abstractmethod
    def get_session(self):
        raise NotImplementedError
