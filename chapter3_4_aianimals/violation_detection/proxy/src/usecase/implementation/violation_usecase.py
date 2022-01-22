from logging import getLogger
from typing import List, Optional

from src.entities.violation import ViolationCreate, ViolationQuery
from src.repository.violation_repository import AbstractViolationRepository
from src.request_object.violation import ViolationCreateRequest, ViolationRequest
from src.response_object.violation import ViolationResponse
from src.usecase.violation_usecase import AbstractViolationUsecase

logger = getLogger(__name__)


class ViolationUsecase(AbstractViolationUsecase):
    def __init__(
        self,
        violation_repository: AbstractViolationRepository,
    ):
        super().__init__(violation_repository=violation_repository)

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
        if data is not None:
            response = ViolationResponse(**data.dict())
            return response
        return None
