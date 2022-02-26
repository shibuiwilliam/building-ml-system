from abc import ABC, abstractmethod
from typing import Optional, Union


class AbstractCache(ABC):
    def __init__(self):
        pass

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
