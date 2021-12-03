from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.user import UserCreate, UserQuery
from src.middleware.strings import get_uuid
from src.repository.user_repository import AbstractUserRepository
from src.request_object.user import UserCreateRequest, UserRequest
from src.response_object.user import UserResponse
from src.usecase.user_usecase import AbstractUserUsecase

logger = getLogger(__name__)


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
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[UserResponse]:
        if limit is None:
            limit = 100
        if offset is None:
            offset = 0
        if limit > 200:
            raise ValueError("limit cannot be more than 200")
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
        record: UserCreateRequest,
    ) -> Optional[UserResponse]:
        user_id = get_uuid()
        create = UserCreate(
            id=user_id,
            handle_name=record.handle_name,
            email_address=record.email_address,
            age=record.age,
            gender=record.gender,
        )
        data = self.user_repository.insert(
            session=session,
            record=create,
            commit=True,
        )
        if data is not None:
            response = UserResponse(**data.dict())
            return response
        return None
