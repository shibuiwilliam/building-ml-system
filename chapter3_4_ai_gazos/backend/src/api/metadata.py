from logging import getLogger

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.registry.container import container
from src.response_object.metadata import MetadataResponse

logger = getLogger(__name__)

router = APIRouter()


@router.get("", response_model=MetadataResponse)
async def get_metadata(
    session: Session = Depends(container.database.get_session),
):
    data = container.metadata_usecase.retrieve(session=session)
    return data
