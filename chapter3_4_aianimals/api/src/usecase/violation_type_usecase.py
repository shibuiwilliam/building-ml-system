from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.violation_type import ViolationTypeCreate, ViolationTypeQuery
from src.middleware.strings import get_uuid
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


class ViolationTypeUsecase(AbstractViolationTypeUsecase):
    def __init__(
        self,
        violation_type_repository: AbstractViolationTypeRepository,
    ):
        super().__init__(violation_type_repository=violation_type_repository)

    def retrieve(
        self,
        session: Session,
        request: Optional[ViolationTypeRequest] = None,
    ) -> List[ViolationTypeResponse]:
        query: Optional[ViolationTypeQuery] = None
        if request is not None:
            query = ViolationTypeQuery(**request.dict())

        data = self.violation_type_repository.select(
            session=session,
            query=query,
        )
        response = [ViolationTypeResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        session: Session,
        request: ViolationTypeCreateRequest,
    ) -> Optional[ViolationTypeResponse]:
        record = ViolationTypeCreate(
            id=get_uuid(),
            name=request.name,
        )
        data = self.violation_type_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        if data is not None:
            response = ViolationTypeResponse(**data.dict())
            return response
        return None
