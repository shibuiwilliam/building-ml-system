import os
from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, Header, UploadFile
from sqlalchemy.orm import Session
from src.configurations import Configurations
from src.middleware.assert_token import token_assertion
from src.middleware.strings import random_str
from src.registry.container import container
from src.request_object.animal import (
    AnimalCreateRequest,
    AnimalRequest,
    AnimalSearchRequest,
    SimilarAnimalSearchRequest,
)
from src.response_object.animal import AnimalResponse, AnimalSearchResponses, SimilarAnimalSearchResponses
from src.response_object.user import UserResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[AnimalResponse])
async def get_animal(
    id: Optional[str] = None,
    name: Optional[str] = None,
    animal_category_id: Optional[str] = None,
    animal_subcategory_id: Optional[str] = None,
    user_id: Optional[str] = None,
    deactivated: Optional[bool] = False,
    limit: int = 100,
    offset: int = 0,
    token: str = Header(...),
    session: Session = Depends(container.database.get_session),
):
    await token_assertion(
        token=token,
        session=session,
    )
    data = container.animal_usecase.retrieve(
        session=session,
        request=AnimalRequest(
            id=id,
            name=name,
            animal_category_id=animal_category_id,
            animal_subcategory_id=animal_subcategory_id,
            user_id=user_id,
            deactivated=deactivated,
        ),
        limit=limit,
        offset=offset,
    )
    return data


@router.get("/liked_by", response_model=List[UserResponse])
async def liked_by(
    animal_id: str,
    limit: int = 100,
    offset: int = 0,
    token: str = Header(...),
    session: Session = Depends(container.database.get_session),
):
    await token_assertion(
        token=token,
        session=session,
    )
    data = container.animal_usecase.liked_by(
        session=session,
        animal_id=animal_id,
        limit=limit,
        offset=offset,
    )
    return data


@router.post("", response_model=AnimalResponse)
async def post_animal(
    background_tasks: BackgroundTasks,
    request: AnimalCreateRequest = Form(...),
    file: UploadFile = File(...),
    token: str = Header(...),
    session: Session = Depends(container.database.get_session),
):
    await token_assertion(
        token=token,
        session=session,
    )
    logger.info(f"register animal: {request}")
    os.makedirs(Configurations.work_directory, exist_ok=True)
    local_file_path = os.path.join(Configurations.work_directory, f"{random_str()}.jpg")
    with open(local_file_path, "wb+") as f:
        f.write(file.file.read())
    logger.info(f"temporarily saved file on {local_file_path}")
    data = container.animal_usecase.register(
        session=session,
        request=request,
        local_file_path=local_file_path,
        background_tasks=background_tasks,
    )
    return data


@router.post("/search", response_model=AnimalSearchResponses)
async def search_animal(
    background_tasks: BackgroundTasks,
    request: Optional[AnimalSearchRequest] = None,
    limit: int = 100,
    offset: int = 0,
    token: str = Header(...),
    session: Session = Depends(container.database.get_session),
):
    _, user_id = await token_assertion(
        token=token,
        session=session,
    )
    if request is None:
        request = AnimalSearchRequest()
    request.user_id = user_id
    logger.info(f"search animal: {request}")
    data = container.animal_usecase.search(
        request=request,
        background_tasks=background_tasks,
        limit=limit,
        offset=offset,
    )
    return data


@router.post("/search/similar", response_model=SimilarAnimalSearchResponses)
async def search_similar_animal(
    request: SimilarAnimalSearchRequest,
    token: str = Header(...),
    session: Session = Depends(container.database.get_session),
):
    _, user_id = await token_assertion(
        token=token,
        session=session,
    )
    request.user_id = user_id
    logger.info(f"search similar animal: {request}")
    data = container.animal_usecase.search_similar_image(
        session=session,
        request=request,
    )
    return data
