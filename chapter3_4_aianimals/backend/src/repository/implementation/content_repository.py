from logging import getLogger
from typing import List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from src.entities.content import ContentCreate, ContentModel, ContentModelWithLike, ContentQuery
from src.entities.user import UserModel
from src.repository.content_repository import AbstractContentRepository
from src.schema.content import Content
from src.schema.like import Like
from src.schema.table import TABLES
from src.schema.user import User

logger = getLogger(__name__)


class ContentRepository(AbstractContentRepository):
    def __init__(self) -> None:
        super().__init__()
        self.table_name = TABLES.CONTENT.value

    def select(
        self,
        session: Session,
        query: Optional[ContentQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[ContentModel]:
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(Content.id == query.id)
            if query.name is not None:
                filters.append(Content.name == query.name)
            if query.user_id is not None:
                filters.append(User.id == query.user_id)
            if query.deactivated is not None:
                filters.append(Content.deactivated == query.deactivated)
        results = (
            session.query(
                Content.id.label("id"),
                User.id.label("user_id"),
                User.handle_name.label("user_handle_name"),
                Content.name.label("name"),
                Content.description.label("description"),
                Content.photo_url.label("photo_url"),
                Content.deactivated.label("deactivated"),
                Content.created_at.label("created_at"),
                Content.updated_at.label("updated_at"),
            )
            .join(
                User,
                User.id == Content.user_id,
                isouter=True,
            )
            .filter(and_(*filters))
            .order_by(Content.id)
            .limit(limit)
            .offset(offset)
        )
        data = [
            ContentModel(
                id=d[0],
                user_id=d[1],
                user_handle_name=d[2],
                name=d[3],
                description=d[4],
                photo_url=d[5],
                deactivated=d[6],
                created_at=d[7],
                updated_at=d[8],
            )
            for d in results
        ]
        return data

    def select_with_like(
        self,
        session: Session,
        query: Optional[ContentQuery],
        order_by_like: bool = True,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[ContentModelWithLike]:
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(Content.id == query.id)
            if query.name is not None:
                filters.append(Content.name == query.name)
            if query.user_id is not None:
                filters.append(User.id == query.user_id)
            if query.deactivated is not None:
                filters.append(Content.deactivated == query.deactivated)
        results = (
            session.query(
                Content.id.label("id"),
                User.id.label("user_id"),
                User.handle_name.label("user_handle_name"),
                Content.name.label("name"),
                Content.description.label("description"),
                Content.photo_url.label("photo_url"),
                Content.deactivated.label("deactivated"),
                Content.created_at.label("created_at"),
                Content.updated_at.label("updated_at"),
                func.count(Like.id).label("like"),
            )
            .join(
                User,
                User.id == Content.user_id,
                isouter=True,
            )
            .join(
                Like,
                Like.content_id == Content.id,
                isouter=True,
            )
            .filter(and_(*filters))
            .group_by(
                Content.id,
                User.id,
                User.handle_name,
                Content.name,
                Content.description,
                Content.photo_url,
                Content.deactivated,
                Content.created_at,
                Content.updated_at,
                Like.content_id,
            )
            .order_by("like" if order_by_like else Content.id)
            .limit(limit)
            .offset(offset)
        )

        data = [
            ContentModelWithLike(
                id=d[0],
                user_id=d[1],
                user_handle_name=d[2],
                name=d[3],
                description=d[4],
                photo_url=d[5],
                deactivated=d[6],
                created_at=d[7],
                updated_at=d[8],
                like=d[9],
            )
            for d in results
        ]
        return data

    def liked_by(
        self,
        session: Session,
        content_id: str,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[UserModel]:
        results = (
            session.query(User)
            .join(
                Like,
                Like.user_id == User.id,
                isouter=True,
            )
            .join(
                Content,
                Content.id == Like.content_id,
                isouter=True,
            )
            .filter(Content.id == content_id)
            .order_by(User.id)
            .limit(limit)
            .offset(offset)
        )
        data = [
            UserModel(
                id=d.id,
                handle_name=d.handle_name,
                email_address=d.email_address,
                age=d.age,
                gender=d.gender,
                deactivated=d.deactivated,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in results
        ]
        return data

    def insert(
        self,
        session: Session,
        record: ContentCreate,
        commit: bool = True,
    ) -> Optional[ContentModel]:
        data = Content(**record.dict())
        session.add(data)
        if commit:
            session.commit()
            session.refresh(data)
            result = self.select(
                session=session,
                query=ContentQuery(id=data.id),
                limit=1,
                offset=0,
            )
            return result[0]
        return None
