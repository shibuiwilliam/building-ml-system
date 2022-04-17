import json
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, List, Optional

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
    model_name: Optional[str] = None

    class Config:
        extra = Extra.forbid


class AbstractSimilarImageSearchService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def search(
        self,
        request: SimilarImageSearchRequest,
    ) -> SimilarImageSearchResponse:
        raise NotImplementedError


class PseudoSimilarImageSearchService(AbstractSimilarImageSearchService):
    def __init__(self):
        pass

    def search(
        self,
        request: SimilarImageSearchRequest,
    ) -> SimilarImageSearchResponse:
        logger.info(f"request for similar image: {request}")
        response = SimilarImageSearchResponse(
            ids=[
                request.id,
                "f6986fbc0de241e48b27af2987e6387a",  # pseudo similar image
                "63cabf72d6614832ba1a376320a4148d",  # pseudo similar image
                "20507ed1b2f54067b8617e55d1d63338",  # pseudo similar image
                "b810c191e8d146dfb62dc839e0eabdbc",  # pseudo similar image
            ]
        )
        logger.info(f"response from similar image search: {response}")
        return response


class SimilarImageSearchService(AbstractSimilarImageSearchService):
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
            return SimilarImageSearchResponse(
                ids=[id],
                model_name=None,
            )
        res_json = res.json()
        response = SimilarImageSearchResponse(**res_json)
        logger.info(f"response from similar image search: {response}")
        return response
