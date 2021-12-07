import os
from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from src.configurations import Configurations
from src.middleware.strings import random_str
from src.registry.container import container
from src.request_object.content import ContentCreateRequest, ContentRequest
from src.response_object.content import ContentResponse, ContentResponseWithLike
from src.response_object.user import UserResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[ContentResponseWithLike])
async def get_content(
    id: Optional[str] = None,
    name: Optional[str] = None,
    user_id: Optional[str] = None,
    deactivated: Optional[bool] = False,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(container.database.get_session),
):
    data = container.content_usecase.retrieve(
        session=session,
        request=ContentRequest(
            id=id,
            name=name,
            user_id=user_id,
            deactivated=deactivated,
        ),
        limit=limit,
        offset=offset,
    )
    return data


@router.get("/liked_by", response_model=List[UserResponse])
async def liked_by(
    content_id: str,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(container.database.get_session),
):
    data = container.content_usecase.liked_by(
        session=session,
        content_id=content_id,
        limit=limit,
        offset=offset,
    )
    return data


@router.post("", response_model=Optional[ContentResponse])
async def post_content(
    request: ContentCreateRequest = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(container.database.get_session),
):
    logger.info(f"register content: {request}")
    os.makedirs(Configurations.work_directory, exist_ok=True)
    local_file_path = os.path.join(Configurations.work_directory, f"{random_str()}.jpg")
    with open(local_file_path, "wb+") as f:
        f.write(file.file.read())
    logger.info(f"temporarily saved file on {local_file_path}")
    data = container.content_usecase.register(
        session=session,
        request=request,
        local_file_path=local_file_path,
    )
    return data
