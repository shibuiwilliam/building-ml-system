from abc import ABC, abstractmethod
from typing import List, Optional

from src.middleware.logger import configure_logger
from src.repository.violation_type_repository import AbstractViolationTypeRepository
from src.request_object.violation_type import ViolationTypeCreateRequest, ViolationTypeRequest
from src.response_object.violation_type import ViolationTypeResponse

logger = configure_logger(__name__)


class AbstractViolationTypeUsecase(ABC):
    def __init__(
        self,
        violation_type_repository: AbstractViolationTypeRepository,
    ):
        self.violation_type_repository = violation_type_repository

    @abstractmethod
    def retrieve(
        self,
        request: Optional[ViolationTypeRequest] = None,
    ) -> List[ViolationTypeResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        request: ViolationTypeCreateRequest,
    ) -> Optional[ViolationTypeResponse]:
        raise NotImplementedError
