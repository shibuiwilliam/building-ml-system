from abc import ABC, abstractmethod
from typing import Dict, Union


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
        id: Union[str, int],
        body: Dict,
    ):
        raise NotImplementedError

    @abstractmethod
    def update_document(
        self,
        index: str,
        id: Union[str, int],
        doc: Dict,
    ):
        raise NotImplementedError

    @abstractmethod
    def is_document_exist(
        self,
        index: str,
        id: Union[str, int],
    ) -> bool:
        raise NotImplementedError
