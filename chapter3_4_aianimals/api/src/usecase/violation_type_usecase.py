from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.repository.violation_type_repository import AbstractViolationTypeRepository
from src.request_object.violation_type import ViolationTypeCreateRequest, ViolationTypeRequest
from src.response_object.violation_type import ViolationTypeResponse

logger = getLogger(__name__)


class AbstractViolationTypeUsecase(ABC):
    def __init__(
        self,
        violation_type_repository: AbstractViolationTypeRepository,
    ):
        self.violation_type_repository = violation_type_repository

    @abstractmethod
    def retrieve(
        self,
        session: Session,
        request: Optional[ViolationTypeRequest] = None,
    ) -> List[ViolationTypeResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        session: Session,
        request: ViolationTypeCreateRequest,
    ) -> Optional[ViolationTypeResponse]:
        raise NotImplementedError
