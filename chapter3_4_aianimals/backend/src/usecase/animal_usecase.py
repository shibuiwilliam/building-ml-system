from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from src.infrastructure.queue import AbstractQueue
from src.infrastructure.storage import AbstractStorage
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.animal_search_repository import AbstractAnimalSearchRepository
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest, AnimalSearchRequest
from src.response_object.animal import AnimalResponse, AnimalSearchResponses
from src.response_object.user import UserResponse

logger = getLogger(__name__)


class AbstractAnimalUsecase(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        animal_search_repository: AbstractAnimalSearchRepository,
        like_repository: AbstractLikeRepository,
        storage_client: AbstractStorage,
        queue: AbstractQueue,
    ):
        self.animal_repository = animal_repository
        self.animal_search_repository = animal_search_repository
        self.like_repository = like_repository
        self.storage_client = storage_client
        self.queue = queue

    @abstractmethod
    def retrieve(
        self,
        session: Session,
        request: Optional[AnimalRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AnimalResponse]:
        raise NotImplementedError

    @abstractmethod
    def liked_by(
        self,
        session: Session,
        animal_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[UserResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        session: Session,
        request: AnimalCreateRequest,
        local_file_path: str,
        background_tasks: BackgroundTasks,
    ) -> Optional[AnimalResponse]:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        session: Session,
        request: Optional[AnimalSearchRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> AnimalSearchResponses:
        raise NotImplementedError
