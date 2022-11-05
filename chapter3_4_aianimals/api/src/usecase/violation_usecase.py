from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.violation import ViolationCreate, ViolationQuery
from src.middleware.strings import get_uuid
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
        session: Session,
        request: Optional[ViolationRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ViolationResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        session: Session,
        request: ViolationCreateRequest,
    ) -> Optional[ViolationResponse]:
        raise NotImplementedError


class ViolationUsecase(AbstractViolationUsecase):
    def __init__(
        self,
        violation_repository: AbstractViolationRepository,
    ):
        super().__init__(violation_repository=violation_repository)

    def retrieve(
        self,
        session: Session,
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
            session=session,
            query=query,
            limit=limit,
            offset=offset,
        )

        response = [ViolationResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        session: Session,
        request: ViolationCreateRequest,
    ) -> Optional[ViolationResponse]:
        record = ViolationCreate(
            id=get_uuid(),
            animal_id=request.animal_id,
            violation_type_id=request.violation_type_id,
            probability=request.probability,
            judge=request.judge,
            is_effective=request.is_effective,
            is_administrator_checked=request.is_administrator_checked,
        )
        data = self.violation_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        if data is not None:
            response = ViolationResponse(**data.dict())
            return response
        return None
