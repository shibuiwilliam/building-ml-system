import os
from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from src.configurations import Configurations
from src.middleware.strings import random_str
from src.registry.container import container
from src.request_object.animal import AnimalCreateRequest, AnimalRequest
from src.response_object.animal import AnimalResponse, AnimalResponseWithLike
from src.response_object.user import UserResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[AnimalResponseWithLike])
async def get_animal(
    id: Optional[str] = None,
    name: Optional[str] = None,
    animal_category_id: Optional[str] = None,
    animal_subcategory_id: Optional[str] = None,
    user_id: Optional[str] = None,
    deactivated: Optional[bool] = False,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(container.database.get_session),
):
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
    session: Session = Depends(container.database.get_session),
):
    data = container.animal_usecase.liked_by(
        session=session,
        animal_id=animal_id,
        limit=limit,
        offset=offset,
    )
    return data


@router.post("", response_model=Optional[AnimalResponse])
async def post_animal(
    background_tasks: BackgroundTasks,
    request: AnimalCreateRequest = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(container.database.get_session),
):
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
