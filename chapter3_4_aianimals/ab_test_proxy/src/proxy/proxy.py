import imp
from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Header
from src.registry.container import container
from src.schema.base_schema import BaseRequest, BaseResponse

logger = getLogger(__name__)

router = APIRouter()


@router.post("/test", response_model=BaseResponse)
async def post_test(
    request: BaseRequest,
):
    return await container.test_service.test(request=request)


@router.post("", response_model=BaseResponse)
async def post(
    request: BaseRequest,
):
    return await container.test_service.route(request=request)
