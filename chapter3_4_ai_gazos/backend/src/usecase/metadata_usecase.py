from abc import ABC, abstractmethod
from logging import getLogger

from src.response_object.metadata import MetadataResponse

logger = getLogger(__name__)


class AbstractMetadataUsecase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def retrieve(self) -> MetadataResponse:
        raise NotImplementedError
