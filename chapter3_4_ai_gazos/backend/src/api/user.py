from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.registry.container import container
from src.request_object.user import UserCreateRequest, UserRequest
from src.response_object.user import UserResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[UserResponse])
async def get_user(
    id: Optional[str] = None,
    handle_name: Optional[str] = None,
    email_address: Optional[str] = None,
    age: Optional[int] = None,
    gender: Optional[int] = None,
    deactivated: Optional[bool] = False,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(container.database.get_session),
):
    data = container.user_usecase.retrieve(
        session=session,
        request=UserRequest(
            id=id,
            handle_name=handle_name,
            email_address=email_address,
            age=age,
            gender=gender,
            deactivated=deactivated,
        ),
        limit=limit,
        offset=offset,
    )
    return data


@router.post("", response_model=Optional[UserResponse])
async def post_user(
    user: UserCreateRequest,
    session: Session = Depends(container.database.get_session),
):
    data = container.user_usecase.register(
        session=session,
        request=user,
    )
    return data
