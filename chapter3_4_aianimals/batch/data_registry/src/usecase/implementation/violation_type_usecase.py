from typing import List, Optional

from src.entities.violation_type import ViolationTypeCreate, ViolationTypeQuery
from src.middleware.logger import configure_logger
from src.repository.violation_type_repository import AbstractViolationTypeRepository
from src.request_object.violation_type import ViolationTypeCreateRequest, ViolationTypeRequest
from src.response_object.violation_type import ViolationTypeResponse
from src.usecase.violation_type_usecase import AbstractViolationTypeUsecase

logger = configure_logger(__name__)


class ViolationTypeUsecase(AbstractViolationTypeUsecase):
    def __init__(
        self,
        violation_type_repository: AbstractViolationTypeRepository,
    ):
        super().__init__(violation_type_repository=violation_type_repository)

    def retrieve(
        self,
        request: Optional[ViolationTypeRequest] = None,
    ) -> List[ViolationTypeResponse]:
        query: Optional[ViolationTypeQuery] = None
        if request is not None:
            query = ViolationTypeQuery(**request.dict())

        data = self.violation_type_repository.select(
            query=query,
        )
        response = [ViolationTypeResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        request: ViolationTypeCreateRequest,
    ) -> Optional[ViolationTypeResponse]:
        logger.info(f"register: {request}")
        exists = self.violation_type_repository.select(
            query=ViolationTypeQuery(id=request.id),
        )
        if len(exists) > 0:
            response = ViolationTypeResponse(**exists[0].dict())
            logger.info(f"exists: {response}")
            return response

        record = ViolationTypeCreate(
            id=request.id,
            name=request.name,
        )
        data = self.violation_type_repository.insert(
            record=record,
            commit=True,
        )
        if data is not None:
            response = ViolationTypeResponse(**data.dict())
            logger.info(f"done register: {response}")
            return response
        return None
