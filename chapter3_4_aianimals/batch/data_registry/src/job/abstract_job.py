import logging
from abc import ABC, abstractmethod


class AbstractJob(ABC):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def run(self):
        raise NotImplementedError
