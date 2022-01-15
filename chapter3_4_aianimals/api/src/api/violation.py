from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from src.middleware.assert_token import token_assertion
from src.registry.container import container
from src.request_object.violation_type import ViolationTypeRequest
from src.response_object.violation_type import ViolationTypeResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("/type", response_model=List[ViolationTypeResponse])
async def get_violation_type(
    id: Optional[int] = None,
    name: Optional[str] = None,
    token: str = Header(...),
    session: Session = Depends(container.database.get_session),
):
    await token_assertion(
        token=token,
        session=session,
    )
    data = container.violation_type_usecase.retrieve(
        session=session,
        request=ViolationTypeRequest(
            id=id,
            name=name,
        ),
    )
    return data
