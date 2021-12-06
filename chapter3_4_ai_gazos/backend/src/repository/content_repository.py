from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.content import ContentCreate, ContentModel, ContentModelWithLike, ContentQuery
from src.entities.user import UserModel

logger = getLogger(__name__)


class AbstractContentRepository(ABC):
    def __init__(self):
        super().__init__()
        pass

    @abstractmethod
    def select(
        self,
        session: Session,
        query: Optional[ContentQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[ContentModel]:
        raise NotImplementedError

    @abstractmethod
    def select_with_like(
        self,
        session: Session,
        query: Optional[ContentQuery],
        order_by_like: bool = True,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[ContentModelWithLike]:
        raise NotImplementedError

    @abstractmethod
    def liked_by(
        self,
        session: Session,
        content_id: str,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[UserModel]:
        raise NotImplementedError

    @abstractmethod
    def insert(
        self,
        session: Session,
        record: ContentCreate,
        commit: bool = True,
    ) -> Optional[ContentModel]:
        raise NotImplementedError
