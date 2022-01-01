from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from src.middleware.assert_token import token_assertion
from src.registry.container import container
from src.request_object.user import UserCreateRequest, UserLoginRequest
from src.response_object.user import UserLoginResponse, UserResponse

logger = getLogger(__name__)

router = APIRouter()


@router.post("/login", response_model=Optional[UserLoginResponse])
async def login_user(
    user: UserLoginRequest,
    session: Session = Depends(container.database.get_session),
):
    data = container.user_usecase.login(
        session=session,
        request=user,
    )
    return data


@router.post("", response_model=Optional[UserResponse])
async def post_user(
    user: UserCreateRequest,
    token: str = Header(...),
    session: Session = Depends(container.database.get_session),
):
    await token_assertion(
        token=token,
        session=session,
    )
    data = container.user_usecase.register(
        session=session,
        request=user,
    )
    return data
