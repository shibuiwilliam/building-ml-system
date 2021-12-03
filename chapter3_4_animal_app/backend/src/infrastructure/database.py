from abc import ABC, abstractmethod


class AbstractDatabase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_session(self):
        raise NotImplementedError
