from logging import getLogger

from fastapi import APIRouter
from src.registry.container import container
from src.schema.base_schema import Request, Response

logger = getLogger(__name__)

router = APIRouter()


@router.post("/test", response_model=Response)
async def post_test(
    request: Request,
):
    logger.info(f"test request: {request}")
    response = await container.test_service.test(request=request)
    logger.info(f"test response: {response}")
    return response


@router.post("", response_model=Response)
async def post(
    request: Request,
):
    logger.info(f"request: {request}")
    response = await container.test_service.route(request=request)
    logger.info(f"response: {response}")
    return response
