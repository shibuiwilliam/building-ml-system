import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum

import pandas as pd
from model import (
    VIOLATION_SORT_BY,
    AbstractAnimalRepository,
    AbstractViolationRepository,
    AbstractViolationTypeRepository,
    AnimalQuery,
    ViolationQuery,
)
from pydantic import BaseModel


class BaseViewModel(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)


class AbstractAnimalViewModel(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
    ):
        self.animal_repository = animal_repository

    @abstractmethod
    def get_animals(
        self,
        ids: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        raise NotImplementedError


class AnimalViewModel(BaseViewModel, AbstractAnimalViewModel):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
    ):
        BaseViewModel.__init__(self)
        AbstractAnimalViewModel.__init__(
            self,
            animal_repository=animal_repository,
        )

    def get_animals(
        self,
        ids: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        query = AnimalQuery(ids=ids)
        limit: int = 200
        offset: int = 0
        animals = []
        while True:
            _animals = self.animal_repository.select(
                animal_query=query,
                limit=limit,
                offset=offset,
            )
            if len(_animals) == 0:
                break
            animals.extend(_animals)
            offset += limit
        animal_dicts = [animal.dict() for animal in animals]
        dataframe = pd.DataFrame(animal_dicts)
        return dataframe


class AbstractViolationTypeViewModel(ABC):
    def __init__(
        self,
        violation_type_repository: AbstractViolationTypeRepository,
    ):
        self.violation_type_repository = violation_type_repository

    @abstractmethod
    def get_violation_types(self) -> Dict[str, str]:
        raise NotImplementedError


class ViolationTypeViewModel(BaseViewModel, AbstractViolationTypeViewModel):
    def __init__(
        self,
        violation_type_repository: AbstractViolationTypeRepository,
    ):
        BaseViewModel.__init__(self)
        AbstractViolationTypeViewModel.__init__(
            self,
            violation_type_repository=violation_type_repository,
        )

        class Cache(BaseModel):
            is_cached: bool = False
            cache: Dict[str, str] = {}
            cached_at: datetime = datetime.now()

        self.__cache: Cache = Cache()

    def get_violation_types(self) -> Dict[str, str]:
        one_hour_ago = datetime.now() - timedelta(hours=-1)
        if self.__cache.is_cached and self.__cache.cached_at > one_hour_ago:
            return self.__cache.cache

        violation_types = self.violation_type_repository.select(
            limit=200,
            offset=0,
        )
        violation_type_dict = {v.name: v.id for v in violation_types}
        self.__cache.is_cached = True
        self.__cache.cache = violation_type_dict
        self.__cache.cached_at = datetime.now()
        return violation_type_dict


class DAYS_FROM(Enum):
    ONE_DAY = 1
    ONE_WEEK = 7
    THIRTY_DAYS = 30
    SIXTY_DAYS = 60
    ONE_HUNDRED_DAYS = 100
    ONE_YEAR = 365

    @staticmethod
    def has_value(value: int) -> bool:
        return value in [v.value for v in DAYS_FROM.__members__.values()]

    @staticmethod
    def get_list() -> List[int]:
        return [v.value for v in DAYS_FROM.__members__.values()]


class AGGREGATE_VIOLATION(Enum):
    UPDATED_AT = "updated_at"

    @staticmethod
    def get_list() -> List[str]:
        return [v.value for v in AGGREGATE_VIOLATION.__members__.values()]


class AbstractViolationViewModel(ABC):
    def __init__(
        self,
        violation_repository: AbstractViolationRepository,
    ):
        self.violation_repository = violation_repository

    @abstractmethod
    def list_violation_sort_by(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def list_days_from(self) -> List[int]:
        raise NotImplementedError

    @abstractmethod
    def list_aggregate_violation(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_violations(
        self,
        ids: Optional[List[str]] = None,
        animal_id: Optional[str] = None,
        violation_type_id: Optional[str] = None,
        judge: Optional[str] = None,
        is_effective: Optional[bool] = None,
        animal_days_from: Optional[int] = None,
        days_from: int = DAYS_FROM.ONE_WEEK.value,
        sort_by: str = VIOLATION_SORT_BY.ID.value,
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def aggregate_violations(
        self,
        violation_df: pd.DataFrame,
        column: str = AGGREGATE_VIOLATION.UPDATED_AT.value,
    ) -> pd.DataFrame:
        raise NotImplementedError


class ViolationViewModel(BaseViewModel, AbstractViolationViewModel):
    def __init__(
        self,
        violation_repository: AbstractViolationRepository,
    ):
        BaseViewModel.__init__(self)
        AbstractViolationViewModel.__init__(
            self,
            violation_repository=violation_repository,
        )

    def list_violation_sort_by(self) -> List[str]:
        return VIOLATION_SORT_BY.get_list()

    def list_days_from(self) -> List[int]:
        return DAYS_FROM.get_list()

    def list_aggregate_violation(self) -> List[str]:
        return AGGREGATE_VIOLATION.get_list()

    def get_violations(
        self,
        ids: Optional[List[str]] = None,
        animal_id: Optional[str] = None,
        violation_type_id: Optional[str] = None,
        judge: Optional[str] = None,
        is_effective: Optional[bool] = None,
        animal_days_from: Optional[int] = None,
        days_from: int = DAYS_FROM.ONE_WEEK.value,
        sort_by: str = VIOLATION_SORT_BY.ID.value,
    ) -> pd.DataFrame:
        query = ViolationQuery(
            ids=ids,
            animal_id=animal_id,
            violation_type_id=violation_type_id,
            judge=judge,
            is_effective=is_effective,
            animal_days_from=animal_days_from,
            days_from=days_from,
        )
        limit: int = 200
        offset: int = 0
        violations = []
        while True:
            _violations = self.violation_repository.select(
                violation_query=query,
                sort_by=sort_by,
                limit=limit,
                offset=offset,
            )
            if len(_violations) == 0:
                break
            violations.extend(_violations)
            offset += limit
        violation_dicts = [violation.dict() for violation in violations]
        dataframe = pd.DataFrame(violation_dicts)
        return dataframe

    def aggregate_violations(
        self,
        violation_df: pd.DataFrame,
        column: str = AGGREGATE_VIOLATION.UPDATED_AT.value,
    ) -> pd.DataFrame:
        aggregated_df = violation_df.groupby(violation_df[column].dt.date).size().reset_index(name="count")
        return aggregated_df
