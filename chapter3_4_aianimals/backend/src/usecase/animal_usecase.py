from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from src.infrastructure.queue import AbstractQueue
from src.infrastructure.storage import AbstractStorage
from src.repository.animal_repository import AbstractAnimalRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest
from src.response_object.animal import AnimalResponse, AnimalResponseWithLike
from src.response_object.user import UserResponse

logger = getLogger(__name__)


class AbstractAnimalUsecase(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        storage_client: AbstractStorage,
        queue: AbstractQueue,
    ):
        self.animal_repository = animal_repository
        self.storage_client = storage_client
        self.queue = queue

    @abstractmethod
    def retrieve(
        self,
        session: Session,
        request: Optional[AnimalRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AnimalResponseWithLike]:
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
