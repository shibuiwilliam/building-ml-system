from typing import List, Optional

from sqlalchemy import and_
from src.entities.user import UserCreate, UserModel, UserQuery
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger
from src.repository.user_repository import AbstractUserRepository
from src.schema.table import TABLES
from src.schema.user import User

logger = configure_logger(__name__)


class UserRepository(AbstractUserRepository):
    def __init__(
        self,
        database: AbstractDatabase,
    ) -> None:
        super().__init__(database=database)
        self.table_name = TABLES.USER.value

    def select(
        self,
        query: Optional[UserQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[UserModel]:
        session = self.database.get_session().__next__()
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(User.id == query.id)
            if query.handle_name is not None:
                filters.append(User.handle_name == query.handle_name)
            if query.email_address is not None:
                filters.append(User.email_address == query.email_address)
            if query.age is not None:
                filters.append(User.age == query.age)
            if query.gender is not None:
                filters.append(User.gender == query.gender)
            if query.deactivated is not None:
                filters.append(User.deactivated == query.deactivated)
        results = session.query(User).filter(and_(*filters)).order_by(User.id).limit(limit).offset(offset)
        data = [
            UserModel(
                id=d.id,
                handle_name=d.handle_name,
                email_address=d.email_address,
                password=d.password,
                age=d.age,
                gender=d.gender,
                deactivated=d.deactivated,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in results
        ]
        session.close()
        return data

    def insert(
        self,
        record: UserCreate,
        commit: bool = True,
    ) -> Optional[UserModel]:
        session = self.database.get_session().__next__()
        data = User(**record.dict())
        session.add(data)
        if commit:
            session.commit()
            session.refresh(data)
            result = self.select(
                query=UserQuery(id=data.id),
                limit=1,
                offset=0,
            )
            session.close()
            return result[0]
        session.close()
        return None
