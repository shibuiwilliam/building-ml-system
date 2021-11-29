from abc import ABC
from logging import getLogger

logger = getLogger(__name__)


class AbstractUsecase(ABC):
    def __init__(self):
        pass
