from typing import Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.constants import CONSTANTS
from src.entities.user import UserLoginQuery
from src.registry.container import container
from starlette.status import HTTP_403_FORBIDDEN


async def token_assertion(
    token: str,
    session: Session,
) -> Tuple[bool, str]:
    try:
        raw_token = container.crypt.decrypt(enc_text=token)
    except Exception:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="authorization failure",
        )

    if CONSTANTS.TOKEN_SPLITTER not in raw_token:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="authorization failure",
        )
    handle_name, password = raw_token.split(CONSTANTS.TOKEN_SPLITTER)

    login_query = UserLoginQuery(
        handle_name=handle_name,
        password=password,
    )
    login_assertion = container.user_repository.assert_login(
        session=session,
        login_query=login_query,
    )
    if login_assertion is None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="authorization failure",
        )
    return True, handle_name
