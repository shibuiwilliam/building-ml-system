import json
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict

import httpx
from pydantic import BaseModel
from src.middleware.json import json_serial
from src.schema.base_schema import BaseAnimalRequest, BaseAnimalResponse, Request, Response
from src.service.ab_test_service import AbstractTestService, Endpoint

logger = getLogger(__name__)


class AnimalIDs(BaseModel):
    animal_ids: Dict[str, Endpoint]
    default_endpoint: Endpoint


class AbstractAnimalTestService(AbstractTestService, ABC):
    def __init__(
        self,
        timeout: float = 10.0,
        retries: int = 2,
    ):
        super().__init__(
            timeout=timeout,
            retries=retries,
        )

    @abstractmethod
    async def test(
        self,
        request: Request[BaseAnimalRequest],
    ) -> Response[BaseAnimalResponse]:
        raise NotImplementedError

    @abstractmethod
    async def route(
        self,
        request: Request[BaseAnimalRequest],
    ) -> Response[BaseAnimalResponse]:
        raise NotImplementedError


class AnimalTestService(AbstractAnimalTestService):
    def __init__(
        self,
        animal_ids: AnimalIDs,
        timeout: float = 10,
        retries: int = 2,
    ):
        super().__init__(
            timeout=timeout,
            retries=retries,
        )
        self.animal_ids = animal_ids
        logger.info(f"initialized user ab test: {self.animal_ids}")

    async def test(
        self,
        request: Request[BaseAnimalRequest],
    ) -> Response[BaseAnimalResponse]:
        return Response[BaseAnimalResponse](
            response=BaseAnimalResponse(
                endpoint="random_test_service",
                response=request.request,
            )
        )

    async def route(
        self,
        request: Request[BaseAnimalRequest],
    ) -> Response[BaseAnimalResponse]:
        endpoint = self.animal_ids.animal_ids.get(request.request.animal_id, self.animal_ids.default_endpoint)
        response = await self.__route(
            request=request.request,
            endpoint=endpoint,
        )
        return Response[BaseAnimalResponse](response=response)

    async def __route(
        self,
        request: BaseAnimalRequest,
        endpoint: Endpoint,
    ) -> BaseAnimalResponse:
        async with httpx.AsyncClient(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            res = await client.post(
                url=endpoint.endpoint,
                headers=self.post_header,
                data=json.dumps(request.request, default=json_serial),
            )
            try:
                res.raise_for_status()
            except httpx.HTTPStatusError as e:
                logger.error(e)
            data = res.json()
            response = BaseAnimalResponse(
                endpoint=endpoint.endpoint,
                response=data,
            )
            return response
