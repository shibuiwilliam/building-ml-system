from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from src.repository.violation_repository import AbstractViolationRepository
from src.request_object.violation import ViolationCreateRequest, ViolationRequest
from src.response_object.violation import ViolationResponse

logger = getLogger(__name__)


class AbstractViolationUsecase(ABC):
    def __init__(
        self,
        violation_repository: AbstractViolationRepository,
    ):
        self.violation_repository = violation_repository

    @abstractmethod
    def retrieve(
        self,
        request: Optional[ViolationRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ViolationResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        request: ViolationCreateRequest,
    ) -> Optional[ViolationResponse]:
        raise NotImplementedError
