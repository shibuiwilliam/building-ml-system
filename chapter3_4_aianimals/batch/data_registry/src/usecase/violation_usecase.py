import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from src.entities.animal import AnimalUpdate
from src.entities.violation import ViolationCreate, ViolationQuery
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.violation_repository import AbstractViolationRepository
from src.request_object.violation import ViolationCreateRequest, ViolationRequest
from src.response_object.violation import ViolationResponse


class AbstractViolationUsecase(ABC):
    def __init__(
        self,
        violation_repository: AbstractViolationRepository,
        animal_repository: AbstractAnimalRepository,
    ):
        self.logger = logging.getLogger(__name__)
        self.violation_repository = violation_repository
        self.animal_repository = animal_repository

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


class ViolationUsecase(AbstractViolationUsecase):
    def __init__(
        self,
        violation_repository: AbstractViolationRepository,
        animal_repository: AbstractAnimalRepository,
    ):
        super().__init__(
            violation_repository=violation_repository,
            animal_repository=animal_repository,
        )

    def retrieve(
        self,
        request: Optional[ViolationRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ViolationResponse]:
        if limit > 200:
            raise ValueError
        query: Optional[ViolationQuery] = None
        if request is not None:
            query = ViolationQuery(**request.dict())
        data = self.violation_repository.select(
            query=query,
            limit=limit,
            offset=offset,
        )

        response = [ViolationResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        request: ViolationCreateRequest,
    ) -> Optional[ViolationResponse]:
        self.logger.info(f"register: {request}")
        exists = self.violation_repository.select(
            query=ViolationQuery(id=request.id),
        )
        if len(exists) > 0:
            response = ViolationResponse(**exists[0].dict())
            self.logger.info(f"exists: {response}")
            return response

        data = self.violation_repository.insert(
            record=ViolationCreate(
                id=request.id,
                animal_id=request.animal_id,
                violation_type_id=request.violation_type_id,
                probability=request.probability,
                judge=request.judge,
                is_effective=request.is_effective,
                is_administrator_checked=request.is_administrator_checked,
            ),
            commit=True,
        )

        self.animal_repository.update(
            record=AnimalUpdate(
                id=request.animal_id,
                deactivated=True,
            )
        )
        if data is not None:
            response = ViolationResponse(**data.dict())
            self.logger.info(f"done register: {response}")
            return response
        return None
