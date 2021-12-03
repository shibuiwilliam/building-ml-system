from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.middleware.database import get_session
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
    animal_category_name: Optional[str] = None,
    animal_subcategory_name: Optional[str] = None,
    user_id: Optional[str] = None,
    deactivated: Optional[bool] = False,
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
    session: Session = Depends(get_session),
):
    data = container.animal_usecase.retrieve(
        session=session,
        request=AnimalRequest(
            id=id,
            name=name,
            animal_category_name=animal_category_name,
            animal_subcategory_name=animal_subcategory_name,
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
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
    session: Session = Depends(get_session),
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
    request: AnimalCreateRequest,
    session: Session = Depends(get_session),
):
    data = container.animal_usecase.register(
        session=session,
        request=request,
    )
    return data
