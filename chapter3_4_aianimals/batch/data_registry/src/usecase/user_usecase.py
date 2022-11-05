import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from src.entities.user import UserCreate, UserQuery
from src.repository.user_repository import AbstractUserRepository
from src.request_object.user import UserCreateRequest, UserRequest
from src.response_object.user import UserResponse


class AbstractUserUsecase(ABC):
    def __init__(
        self,
        user_repository: AbstractUserRepository,
    ):
        self.logger = logging.getLogger(__name__)
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
        self.logger.info(f"register: {request}")
        exists = self.user_repository.select(
            query=UserQuery(id=request.id),
        )
        if len(exists) > 0:
            response = UserResponse(**exists[0].dict())
            self.logger.info(f"exists: {response}")
            return response

        data = self.user_repository.insert(
            record=UserCreate(
                id=request.id,
                handle_name=request.handle_name,
                email_address=request.email_address,
                password=request.password,
                age=request.age,
                gender=request.gender,
            ),
            commit=True,
        )
        if data is not None:
            response = UserResponse(**data.dict())
            self.logger.info(f"done register: {response}")
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
            self.logger.info(f"bulk register user: {i} to {i+200}")
