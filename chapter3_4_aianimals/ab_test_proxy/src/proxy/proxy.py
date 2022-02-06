import imp
from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Header
from src.schema.base_schema import Request, Response

logger = getLogger(__name__)

router = APIRouter()


@router.post("", response_model=Response)
async def post(
    background_tasks: BackgroundTasks,
    request: Request,
):
    pass
