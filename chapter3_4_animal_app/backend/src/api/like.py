from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.middleware.database import get_session
from src.registry.container import container
from src.request_object.like import LikeCreateRequest, LikeDeleteRequest, LikeRequest
from src.response_object.like import LikeResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[LikeResponse])
async def get_like(
    id: Optional[str] = None,
    animal_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session: Session = Depends(get_session),
):
    data = container.like_usecase.retrieve(
        session=session,
        request=LikeRequest(
            id=id,
            animal_id=animal_id,
            user_id=user_id,
        ),
    )
    return data


@router.post("", response_model=Optional[LikeResponse])
async def post_like(
    like: LikeCreateRequest,
    session: Session = Depends(get_session),
):
    data = container.like_usecase.register(
        session=session,
        record=like,
    )
    return data


@router.delete("", response_model=None)
async def delete_like(
    like_id: str,
    session: Session = Depends(get_session),
):
    container.like_usecase.delete(
        session=session,
        record=LikeDeleteRequest(
            id=like_id,
        ),
    )
    return None
