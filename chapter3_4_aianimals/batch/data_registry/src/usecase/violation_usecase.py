from abc import ABC, abstractmethod
from typing import List, Optional

from src.entities.animal import AnimalUpdate
from src.entities.violation import ViolationCreate, ViolationQuery
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.violation_repository import AbstractViolationRepository
from src.request_object.violation import ViolationCreateRequest, ViolationRequest
from src.response_object.violation import ViolationResponse

logger = configure_logger(__name__)


class AbstractViolationUsecase(ABC):
    def __init__(
        self,
        violation_repository: AbstractViolationRepository,
        animal_repository: AbstractAnimalRepository,
    ):
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
        logger.info(f"register: {request}")
        exists = self.violation_repository.select(
            query=ViolationQuery(id=request.id),
        )
        if len(exists) > 0:
            response = ViolationResponse(**exists[0].dict())
            logger.info(f"exists: {response}")
            return response

        record = ViolationCreate(
            id=request.id,
            animal_id=request.animal_id,
            violation_type_id=request.violation_type_id,
            probability=request.probability,
            judge=request.judge,
            is_effective=request.is_effective,
        )
        data = self.violation_repository.insert(
            record=record,
            commit=True,
        )
        animal_update = AnimalUpdate(
            id=request.animal_id,
            deactivated=True,
        )
        self.animal_repository.update(record=animal_update)
        if data is not None:
            response = ViolationResponse(**data.dict())
            logger.info(f"done register: {response}")
            return response
        return None
