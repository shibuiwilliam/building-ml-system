from logging import getLogger

from src.constants import GENDER
from src.response_object.metadata import MetadataResponse
from src.usecase.metadata_usecase import AbstractMetadataUsecase

logger = getLogger(__name__)


class MetadataUsecase(AbstractMetadataUsecase):
    def __init__(
        self,
    ):
        super().__init__()
        pass

    def retrieve(self) -> MetadataResponse:
        gender = GENDER.get_list()
        response = MetadataResponse(gender=gender)
        return response
