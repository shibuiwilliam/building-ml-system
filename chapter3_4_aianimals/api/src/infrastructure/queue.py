from abc import ABC, abstractmethod
from typing import Optional, Tuple, Union


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

    @abstractmethod
    def set(
        self,
        key: str,
        value: Union[str, int, float, bool, bytes],
        expire_second: int = 600,
    ):
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        key: str,
    ) -> Optional[Union[str, int, float, bool, bytes]]:
        raise NotImplementedError
