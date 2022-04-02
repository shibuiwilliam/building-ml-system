from logging import getLogger

from fastapi import APIRouter, BackgroundTasks, Depends, Header
from sqlalchemy.orm import Session
from src.middleware.assert_token import token_assertion
from src.registry.container import container
from src.request_object.access_log import AccessLogCreateRequest

logger = getLogger(__name__)

router = APIRouter()


async def register_access_log(
    request: AccessLogCreateRequest,
    token: str,
    session: Session,
):
    _, user_id = await token_assertion(
        token=token,
        session=session,
    )
    request.user_id = user_id
    logger.info(f"add access log for {request}")
    container.access_log_usecase.register(
        session=session,
        request=request,
    )


@router.post("", response_model=None)
async def post_access_log(
    background_tasks: BackgroundTasks,
    request: AccessLogCreateRequest,
    token: str = Header(...),
    session: Session = Depends(container.database.get_session),
):
    background_tasks.add_task(
        register_access_log,
        request,
        token,
        session,
    )
