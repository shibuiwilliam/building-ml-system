from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.schema.abstract_schema import AbstractCreate, AbstractModel, AbstractQuery

logger = getLogger(__name__)


class AbstractUsecase(ABC):
    def __init__(self):
        pass
