from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.registry.container import container
from src.request_object.like import LikeCreateRequest, LikeDeleteRequest, LikeRequest
from src.response_object.like import LikeResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[LikeResponse])
async def get_like(
    id: Optional[str] = None,
    content_id: Optional[str] = None,
    user_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(container.database.get_session),
):
    request = LikeRequest(
        id=id,
        content_id=content_id,
        user_id=user_id,
    )
    logger.info(f"get like for {request}")
    data = container.like_usecase.retrieve(
        session=session,
        request=request,
        limit=limit,
        offset=offset,
    )
    return data


@router.post("", response_model=Optional[LikeResponse])
async def post_like(
    request: LikeCreateRequest,
    session: Session = Depends(container.database.get_session),
):
    logger.info(f"add like for {request}")
    data = container.like_usecase.register(
        session=session,
        request=request,
    )
    return data


@router.delete("", response_model=str)
async def delete_like(
    like_id: str,
    session: Session = Depends(container.database.get_session),
):
    logger.info(f"unlike for {like_id}")
    container.like_usecase.delete(
        session=session,
        request=LikeDeleteRequest(
            id=like_id,
        ),
    )
    return like_id
