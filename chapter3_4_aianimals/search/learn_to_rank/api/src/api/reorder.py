from logging import getLogger

from fastapi import APIRouter, BackgroundTasks
from src.registry.container import EmptyContainer
from src.registry.registry import container
from src.schema.animal import AnimalRequest, AnimalRequestResponse, AnimalResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=AnimalRequestResponse)
async def get_reorder_definition():
    return AnimalRequestResponse()


@router.post("", response_model=AnimalResponse)
async def post_reorder(
    background_tasks: BackgroundTasks,
    request: AnimalRequest,
):
    if isinstance(container, EmptyContainer):
        return AnimalResponse(ids=request.ids)
    else:
        data = container.reorder_usecase.reorder(
            request=request,
            background_tasks=background_tasks,
        )
        return data
