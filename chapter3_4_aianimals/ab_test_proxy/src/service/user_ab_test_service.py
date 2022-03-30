import json
from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict

import httpx
from pydantic import BaseModel
from src.middleware.json import json_serial
from src.schema.base_schema import BaseUserRequest, BaseUserResponse, Request, Response
from src.service.ab_test_service import AbstractTestService, Endpoint

logger = getLogger(__name__)


class UserIDs(BaseModel):
    user_ids: Dict[str, Endpoint]
    default_endpoint: Endpoint


class AbstractUserTestService(AbstractTestService, ABC):
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
        request: Request[BaseUserRequest],
    ) -> Response[BaseUserResponse]:
        raise NotImplementedError

    @abstractmethod
    async def route(
        self,
        request: Request[BaseUserRequest],
    ) -> Response[BaseUserResponse]:
        raise NotImplementedError


class UserTestService(AbstractUserTestService):
    def __init__(
        self,
        user_ids: UserIDs,
        timeout: float = 10,
        retries: int = 2,
    ):
        super().__init__(
            timeout=timeout,
            retries=retries,
        )
        self.user_ids = user_ids
        logger.info(f"initialized user ab test: {self.user_ids}")

    async def test(
        self,
        request: Request[BaseUserRequest],
    ) -> Response[BaseUserResponse]:
        return Response[BaseUserResponse](
            response=BaseUserResponse(
                endpoint="random_test_service",
                response=request.request,
            ),
        )

    async def route(
        self,
        request: Request[BaseUserRequest],
    ) -> Response[BaseUserResponse]:
        endpoint = self.user_ids.user_ids.get(request.request.user_id, self.user_ids.default_endpoint)
        response = await self.__route(
            request=request,
            endpoint=endpoint,
        )
        return Response[BaseUserResponse](response=response)

    async def __route(
        self,
        request: BaseUserRequest,
        endpoint: Endpoint,
    ) -> BaseUserResponse:
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
            response = BaseUserResponse(
                endpoint=endpoint.endpoint,
                response=data,
            )
            return response
