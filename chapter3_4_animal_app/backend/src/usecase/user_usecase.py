from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.repository.user_repository import UserRepository
from src.schema.user import UserCreate, UserModel, UserQuery
from src.usecase.abstract_usecase import AbstractUsecase

logger = getLogger(__name__)


class UserUsecase(AbstractUsecase):
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        super().__init__()
        self.user_repository = user_repository

    def retrieve(
        self,
        session: Session,
        id: Optional[str] = None,
        handle_name: Optional[str] = None,
        email_address: Optional[str] = None,
        age: Optional[int] = None,
        gender: Optional[int] = None,
        deactivated: Optional[bool] = False,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[UserModel]:
        data = self.user_repository.select(
            session=session,
            query=UserQuery(
                id=id,
                handle_name=handle_name,
                email_address=email_address,
                age=age,
                gender=gender,
                deactivated=deactivated,
            ),
            limit=limit,
            offset=offset,
        )
        return data

    def register(
        self,
        session: Session,
        record: UserCreate,
    ) -> Optional[UserModel]:
        data = self.user_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        return data
