from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest
from src.response_object.animal import AnimalResponse, AnimalResponseWithLike

logger = configure_logger(__name__)


class AbstractAnimalUsecase(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
    ):
        self.animal_repository = animal_repository

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
    def register(
        self,
        session: Session,
        request: AnimalCreateRequest,
    ) -> Optional[AnimalResponse]:
        raise NotImplementedError
