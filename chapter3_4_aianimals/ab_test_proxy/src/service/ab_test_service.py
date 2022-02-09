from abc import ABC, abstractmethod
from enum import Enum
from logging import getLogger
from typing import Dict, List, Optional

import httpx
from pydantic import BaseModel
from src.schema.base_schema import Request, Response

logger = getLogger(__name__)


class ABTestType(Enum):
    RANDOM = "random"
    USER = "user"
    ANIMAL = "animal"

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in ABTestType.__members__.values()]

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in ABTestType.__members__.values()]

    @staticmethod
    def value_to_key(value: Optional[str] = None) -> Optional[Enum]:
        if value is None:
            return None
        for v in [v for v in ABTestType.__members__.values()]:
            if value == v.value:
                return v
        return None


class Endpoint(BaseModel):
    name: Optional[str]
    endpoint: str


class AbstractTestService(ABC):
    def __init__(
        self,
        timeout: float = 10.0,
        retries: int = 2,
    ):
        self.timeout = timeout
        self.retries = retries
        self.transport = httpx.AsyncHTTPTransport(
            retries=self.retries,
        )
        self.post_header: Dict[str, str] = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    @abstractmethod
    async def test(
        self,
        request: Request,
    ) -> Response:
        raise NotImplementedError

    @abstractmethod
    async def route(
        self,
        request: Request,
    ) -> Response:
        raise NotImplementedError
