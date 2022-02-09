import json
import random
from abc import ABC, abstractmethod
from logging import getLogger

import httpx
from pydantic import BaseModel, root_validator
from src.middleware.json import json_serial
from src.schema.base_schema import BaseRandomABTestRequest, BaseRandomABTestResponse, Request, Response
from src.service.ab_test_service import AbstractTestService, Endpoint

logger = getLogger(__name__)


class DistributionRate(BaseModel):
    endpoint: Endpoint
    rate: float


class RandomDistribution(BaseModel):
    endpoint_a: DistributionRate
    endpoint_b: DistributionRate

    @root_validator
    def validate_rate(cls, values):
        endpoint_a = values.get("endpoint_a")
        endpoint_b = values.get("endpoint_b")
        if endpoint_a.rate + endpoint_b.rate != 1.0:
            raise ValueError("sum rates must be equal to 1.0")
        return values


class AbstractRandomABTestService(AbstractTestService, ABC):
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
        request: Request[BaseRandomABTestRequest],
    ) -> Response[BaseRandomABTestResponse]:
        raise NotImplementedError

    @abstractmethod
    async def route(
        self,
        request: Request[BaseRandomABTestRequest],
    ) -> Response[BaseRandomABTestResponse]:
        raise NotImplementedError

    @abstractmethod
    async def route_a(
        self,
        request: Request[BaseRandomABTestRequest],
    ) -> Response[BaseRandomABTestResponse]:
        raise NotImplementedError

    @abstractmethod
    async def route_b(
        self,
        request: Request[BaseRandomABTestRequest],
    ) -> Response[BaseRandomABTestResponse]:
        raise NotImplementedError


class RandomABTestService(AbstractRandomABTestService):
    def __init__(
        self,
        random_distribution: RandomDistribution,
        timeout: float = 10.0,
        retries: int = 2,
    ):
        super().__init__(
            timeout=timeout,
            retries=retries,
        )
        self.random_distribution = random_distribution
        logger.info(f"initialized random distribution: {self.random_distribution}")

    async def test(
        self,
        request: Request[BaseRandomABTestRequest],
    ) -> Response[BaseRandomABTestResponse]:
        return Response[BaseRandomABTestResponse](
            response=BaseRandomABTestResponse(
                endpoint="random_test_service",
                response=request.request,
            )
        )

    async def route(
        self,
        request: Request[BaseRandomABTestRequest],
    ) -> Response[BaseRandomABTestResponse]:
        if random.random() < self.random_distribution.endpoint_a.rate:
            return await self.route_a(request=request)
        else:
            return await self.route_b(request=request)

    async def route_a(
        self,
        request: Request[BaseRandomABTestRequest],
    ) -> Response[BaseRandomABTestResponse]:
        response = await self.__route(
            request=request.request,
            endpoint=self.random_distribution.endpoint_a.endpoint,
        )
        return Response[BaseRandomABTestResponse](response=response)

    async def route_b(
        self,
        request: Request[BaseRandomABTestRequest],
    ) -> Response[BaseRandomABTestResponse]:
        response = await self.__route(
            request=request.request,
            endpoint=self.random_distribution.endpoint_b.endpoint,
        )
        return Response[BaseRandomABTestResponse](response=response)

    async def __route(
        self,
        request: BaseRandomABTestRequest,
        endpoint: Endpoint,
    ) -> BaseRandomABTestResponse:
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
            response = BaseRandomABTestResponse(
                endpoint=endpoint.endpoint,
                response=data,
            )
            return response
