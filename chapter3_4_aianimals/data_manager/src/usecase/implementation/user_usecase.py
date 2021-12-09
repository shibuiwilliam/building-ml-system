from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.user import UserCreate, UserQuery
from src.middleware.logger import configure_logger
from src.middleware.strings import get_uuid
from src.repository.user_repository import AbstractUserRepository
from src.request_object.user import UserCreateRequest, UserRequest
from src.response_object.user import UserResponse
from src.usecase.user_usecase import AbstractUserUsecase

logger = configure_logger(__name__)


class UserUsecase(AbstractUserUsecase):
    def __init__(
        self,
        user_repository: AbstractUserRepository,
    ):
        super().__init__(user_repository=user_repository)

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
