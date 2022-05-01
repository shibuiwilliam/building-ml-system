import logging
from abc import ABC, abstractmethod
from typing import Optional

from src.entities.animal import AnimalUpdate
from src.entities.violation import ViolationCreate
from src.middleware.strings import get_uuid
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.violation_repository import AbstractViolationRepository
from src.repository.violation_type_repository import AbstractViolationTypeRepository
from src.request_object.violation import ViolationCreateRequest
from src.response_object.violation import ViolationResponse


class AbstractViolationUsecase(ABC):
    def __init__(
        self,
        violation_repository: AbstractViolationRepository,
        violation_type_repository: AbstractViolationTypeRepository,
        animal_repository: AbstractAnimalRepository,
    ):
        self.logger = logging.getLogger(__name__)
        self.violation_repository = violation_repository
        self.violation_type_repository = violation_type_repository
        self.animal_repository = animal_repository

    @abstractmethod
    def register(
        self,
        request: ViolationCreateRequest,
    ) -> Optional[ViolationResponse]:
        raise NotImplementedError


class ViolationUsecase(AbstractViolationUsecase):
    def __init__(
        self,
        violation_repository: AbstractViolationRepository,
        violation_type_repository: AbstractViolationTypeRepository,
        animal_repository: AbstractAnimalRepository,
    ):
        super().__init__(
            violation_repository=violation_repository,
            violation_type_repository=violation_type_repository,
            animal_repository=animal_repository,
        )

    def register(
        self,
        request: ViolationCreateRequest,
    ) -> Optional[ViolationResponse]:
        violation_id = get_uuid()
        record = ViolationCreate(
            id=violation_id,
            animal_id=request.animal_id,
            violation_type_id=request.violation_type_id,
            probability=request.probability,
            judge=request.judge,
            is_effective=request.is_effective,
            is_administrator_checked=request.is_administrator_checked,
        )
        data = self.violation_repository.insert(
            record=record,
            commit=True,
        )

        if record.is_effective and record.probability > 0.9:
            animal_update = AnimalUpdate(
                id=request.animal_id,
                deactivated=True,
            )
            self.animal_repository.update(record=animal_update)
        if data is not None:
            response = ViolationResponse(**data.dict())
            return response
        return None
