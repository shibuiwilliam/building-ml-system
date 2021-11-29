from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.middleware.database import get_session
from src.registry.container import container
from src.schema.user import UserCreate, UserModel

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=List[UserModel])
async def get_user(
    id: Optional[str] = None,
    handle_name: Optional[str] = None,
    email_address: Optional[str] = None,
    age: Optional[int] = None,
    gender: Optional[int] = None,
    deactivated: Optional[bool] = False,
    session: Session = Depends(get_session),
):
    data = container.user_usecase.retrieve(
        session=session,
        id=id,
        handle_name=handle_name,
        email_address=email_address,
        age=age,
        gender=gender,
        deactivated=deactivated,
    )
    return data


@router.post("", response_model=Optional[UserModel])
async def create_user(
    user: UserCreate,
    session: Session = Depends(get_session),
):
    data = container.user_usecase.register(
        session=session,
        record=user,
    )
    return data
