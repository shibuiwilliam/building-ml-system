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
    return await container.test_service.test(request=request)


@router.post("", response_model=Response)
async def post(
    request: Request,
):
    return await container.test_service.route(request=request)
