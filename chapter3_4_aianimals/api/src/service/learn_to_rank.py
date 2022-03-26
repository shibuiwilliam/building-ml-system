import json
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, List, Optional

import httpx
from pydantic import BaseModel, Extra
from src.configurations import Configurations

logger = getLogger(__name__)


class LearnToRankRequest(BaseModel):
    ids: List[str]
    query_phrases: List[str] = []
    query_animal_category_id: Optional[int] = None
    query_animal_subcategory_id: Optional[int] = None

    class Config:
        extra = Extra.forbid


class LearnToRankResponse(BaseModel):
    ids: List[str]

    class Config:
        extra = Extra.forbid


class AbstractLearnToRank(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def reorder(
        self,
        request: LearnToRankRequest,
    ) -> LearnToRankResponse:
        raise NotImplementedError


class LearnToRankClient(AbstractLearnToRank):
    def __init__(
        self,
        timeout: float = 10.0,
        retries: int = 3,
    ):
        self.timeout = timeout
        self.transport = httpx.HTTPTransport(
            retries=retries,
        )
        self.url = Configurations.learn_to_rank_url
        self.post_header: Dict[str, str] = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def reorder(
        self,
        request: LearnToRankRequest,
    ) -> LearnToRankResponse:
        logger.info(f"request for learn to rank: {request}")
        if self.url is None:
            return LearnToRankResponse(ids=request.ids)
        with httpx.Client(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            res = client.post(
                url=self.url,
                data=json.dumps(request),
                headers=self.post_header,
            )
        if res.status_code != 200:
            return LearnToRankResponse(ids=request.ids)
        response = LearnToRankResponse(**res.json())
        logger.info(f"response for learn to rank: {response}")
        return response
