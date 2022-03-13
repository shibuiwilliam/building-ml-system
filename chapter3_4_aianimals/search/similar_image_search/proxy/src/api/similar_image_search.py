from logging import getLogger

from fastapi import APIRouter, BackgroundTasks
from src.registry.container import container
from src.schema.animal import AnimalRequest, AnimalRequestResponse, AnimalResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=AnimalRequestResponse)
async def get_similar_image_search_definition():
    return AnimalRequestResponse()


@router.post("", response_model=AnimalResponse)
async def post_similar_image_search(
    background_tasks: BackgroundTasks,
    request: AnimalRequest,
):
    data = container.search_similar_image_usecase.search(
        request=request,
        background_tasks=background_tasks,
    )
    return data
