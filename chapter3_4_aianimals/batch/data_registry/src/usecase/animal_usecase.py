from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.infrastructure.search import AbstractSearch
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest
from src.response_object.animal import AnimalResponse, AnimalResponseWithLike

logger = configure_logger(__name__)


class AbstractAnimalUsecase(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        like_repository: AbstractLikeRepository,
        search: AbstractSearch,
        messaging: RabbitmqMessaging,
    ):
        self.animal_repository = animal_repository
        self.like_repository = like_repository
        self.search = search
        self.messaging = messaging

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
    def register_document(
        self,
        animal_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def register_document_from_queue(self):
        raise NotImplementedError
