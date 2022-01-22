from abc import ABC, abstractmethod
from logging import getLogger
from typing import Optional

from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.violation_repository import AbstractViolationRepository
from src.repository.violation_type_repository import AbstractViolationTypeRepository
from src.request_object.violation import ViolationCreateRequest
from src.response_object.violation import ViolationResponse

logger = getLogger(__name__)


class AbstractViolationUsecase(ABC):
    def __init__(
        self,
        violation_repository: AbstractViolationRepository,
        violation_type_repository: AbstractViolationTypeRepository,
        animal_repository: AbstractAnimalRepository,
    ):
        self.violation_repository = violation_repository
        self.violation_type_repository = violation_type_repository
        self.animal_repository = animal_repository

    @abstractmethod
    def register(
        self,
        request: ViolationCreateRequest,
    ) -> Optional[ViolationResponse]:
        raise NotImplementedError
