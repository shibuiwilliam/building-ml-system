from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from src.entities.user import UserCreate, UserQuery
from src.middleware.logger import configure_logger
from src.repository.user_repository import AbstractUserRepository
from src.request_object.user import UserCreateRequest, UserRequest
from src.response_object.user import UserResponse

logger = configure_logger(__name__)


class AbstractUserUsecase(ABC):
    def __init__(
        self,
        user_repository: AbstractUserRepository,
    ):
        self.user_repository = user_repository

    @abstractmethod
    def retrieve(
        self,
        request: Optional[UserRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[UserResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        request: UserCreateRequest,
    ) -> Optional[UserResponse]:
        raise NotImplementedError

    @abstractmethod
    def bulk_register(
        self,
        requests: List[UserCreateRequest],
    ):
        raise NotImplementedError


class UserUsecase(AbstractUserUsecase):
    def __init__(
        self,
        user_repository: AbstractUserRepository,
    ):
        super().__init__(user_repository=user_repository)

    def retrieve(
        self,
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
            query=query,
            limit=limit,
            offset=offset,
        )

        response = [UserResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        request: UserCreateRequest,
    ) -> Optional[UserResponse]:
        logger.info(f"register: {request}")
        exists = self.user_repository.select(
            query=UserQuery(id=request.id),
        )
        if len(exists) > 0:
            response = UserResponse(**exists[0].dict())
            logger.info(f"exists: {response}")
            return response

        record = UserCreate(
            id=request.id,
            handle_name=request.handle_name,
            email_address=request.email_address,
            password=request.password,
            age=request.age,
            gender=request.gender,
        )
        data = self.user_repository.insert(
            record=record,
            commit=True,
        )
        if data is not None:
            response = UserResponse(**data.dict())
            logger.info(f"done register: {response}")
            return response
        return None

    def bulk_register(
        self,
        requests: List[UserCreateRequest],
    ):
        records = [
            UserCreate(
                id=request.id,
                handle_name=request.handle_name,
                email_address=request.email_address,
                password=request.password,
                age=request.age,
                gender=request.gender,
                created_at=request.created_at,
                updated_at=datetime.now(),
            )
            for request in requests
        ]
        for i in range(0, len(records), 200):
            self.user_repository.bulk_insert(
                records=records[i : i + 200],
                commit=True,
            )
            logger.info(f"bulk register user: {i} to {i+200}")
