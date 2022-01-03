from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.constants import CONSTANTS
from src.entities.user import UserCreate, UserLoginQuery, UserQuery
from src.middleware.crypt import AbstractCrypt
from src.middleware.strings import get_uuid
from src.repository.user_repository import AbstractUserRepository
from src.request_object.user import UserCreateRequest, UserLoginRequest, UserRequest
from src.response_object.user import UserLoginResponse, UserResponse
from src.usecase.user_usecase import AbstractUserUsecase

logger = getLogger(__name__)


class UserUsecase(AbstractUserUsecase):
    def __init__(
        self,
        user_repository: AbstractUserRepository,
        crypt: AbstractCrypt,
    ):
        super().__init__(
            user_repository=user_repository,
            crypt=crypt,
        )

    def retrieve(
        self,
        session: Session,
        request: Optional[UserRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[UserResponse]:
        if limit > 200:
            raise ValueError
        query: Optional[UserQuery] = None
        if request is not None:
            query = UserQuery(**request.dict())
        data = self.user_repository.select(
            session=session,
            query=query,
            limit=limit,
            offset=offset,
        )

        response = [UserResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        session: Session,
        request: UserCreateRequest,
    ) -> Optional[UserResponse]:
        record = UserCreate(
            id=get_uuid(),
            handle_name=request.handle_name,
            email_address=request.email_address,
            age=request.age,
            gender=request.gender,
        )
        data = self.user_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        if data is not None:
            response = UserResponse(**data.dict())
            return response
        return None

    def login(
        self,
        session: Session,
        request: UserLoginRequest,
    ) -> Optional[UserLoginResponse]:
        if request.handle_name is None and request.email_address is None:
            raise ValueError("either handle_name or email_address must be specified")
        if (request.handle_name == "" or request.email_address == "") and request.password == "":
            raise ValueError("handle_name and password must be specified")
        login_query = UserLoginQuery(
            handle_name=request.handle_name,
            email_address=request.email_address,
            password=request.password,
        )
        login_assertion = self.user_repository.assert_login(
            session=session,
            login_query=login_query,
        )
        if login_assertion is None:
            return None

        raw_text = f"{login_assertion.handle_name}{CONSTANTS.TOKEN_SPLITTER}{login_assertion.password}"
        encrypted_text = self.crypt.encrypt(text=raw_text)
        return UserLoginResponse(
            user_id=login_assertion.id,
            token=encrypted_text,
        )
