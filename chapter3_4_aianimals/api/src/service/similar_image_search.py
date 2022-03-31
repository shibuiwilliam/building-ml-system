import json
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, List

import httpx
from pydantic import BaseModel, Extra
from src.configurations import Configurations

logger = getLogger(__name__)


class SimilarImageSearchRequest(BaseModel):
    id: str

    class Config:
        extra = Extra.forbid


class SimilarImageSearchResponse(BaseModel):
    ids: List[str]

    class Config:
        extra = Extra.forbid


class AbstractSimilarImageSearch(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def search(
        self,
        request: SimilarImageSearchRequest,
    ) -> SimilarImageSearchResponse:
        raise NotImplementedError


class SimilarImageSearch(AbstractSimilarImageSearch):
    def __init__(
        self,
        timeout: float = 10.0,
        retries: int = 3,
    ):
        self.timeout = timeout
        self.transport = httpx.HTTPTransport(
            retries=retries,
        )
        self.url = Configurations.similar_image_search_url
        self.post_header: Dict[str, str] = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def search(
        self,
        request: SimilarImageSearchRequest,
    ) -> SimilarImageSearchResponse:
        logger.info(f"request for similar image: {request}")
        if self.url is None:
            logger.info(f"skip request similar image search")
            return SimilarImageSearchResponse(ids=[id])

        with httpx.Client(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            req = request.dict()
            res = client.post(
                url=self.url,
                data=json.dumps(req),
                headers=self.post_header,
            )
        if res.status_code != 200:
            logger.error(f"failed to request similar image search: {res}")
            return SimilarImageSearchResponse(ids=[id])
        res_json = res.json()
        response = SimilarImageSearchResponse(**res_json)
        logger.info(f"response from similar image search: {response}")
        return response
