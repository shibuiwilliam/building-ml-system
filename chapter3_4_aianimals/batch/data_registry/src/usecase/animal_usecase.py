from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from src.infrastructure.queue import AbstractQueue
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest
from src.response_object.animal import AnimalResponse, AnimalResponseWithLike

logger = configure_logger(__name__)


class AbstractAnimalUsecase(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        queue: AbstractQueue,
    ):
        self.animal_repository = animal_repository
        self.queue = queue

    @abstractmethod
    def retrieve(
        self,
        request: Optional[AnimalRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AnimalResponseWithLike]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        request: AnimalCreateRequest,
    ) -> Optional[AnimalResponse]:
        raise NotImplementedError

    @abstractmethod
    def create_index(self):
        raise NotImplementedError

    @abstractmethod
    def get_index(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def index_exists(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def register_index(
        self,
        animal_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def register_index_from_queue(self):
        raise NotImplementedError
