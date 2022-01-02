from logging import getLogger
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
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
    try:
        data = container.user_usecase.login(
            session=session,
            request=user,
        )
        return data
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f"authorization failed: {e}",
        )


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
