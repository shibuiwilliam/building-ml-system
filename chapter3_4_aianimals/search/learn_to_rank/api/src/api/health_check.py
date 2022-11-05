from logging import getLogger

from fastapi import APIRouter

logger = getLogger(__name__)

router = APIRouter()


@router.get("")
async def health():
    return {"health": "ok"}
