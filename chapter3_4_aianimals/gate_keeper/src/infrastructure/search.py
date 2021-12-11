from abc import ABC, abstractmethod
from typing import Dict, Tuple


class AbstractSearch(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_index(
        self,
        index: str,
        body: Dict,
    ):
        raise NotImplementedError

    @abstractmethod
    def get_index(
        self,
        index: str,
    ) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def index_exists(
        self,
        index: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create_document(
        self,
        index: str,
        id: Tuple[str, int],
        body: Dict,
    ):
        raise NotImplementedError
