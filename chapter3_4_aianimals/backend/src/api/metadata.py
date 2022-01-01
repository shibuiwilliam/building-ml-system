from logging import getLogger

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from src.middleware.assert_token import token_assertion
from src.registry.container import container
from src.response_object.metadata import MetadataResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=MetadataResponse)
async def get_metadata(
    token: str = Header(...),
    session: Session = Depends(container.database.get_session),
):
    await token_assertion(
        token=token,
        session=session,
    )
    data = container.metadata_usecase.retrieve(session=session)
    return data
