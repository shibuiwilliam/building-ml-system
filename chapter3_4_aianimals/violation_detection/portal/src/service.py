import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional

import pandas as pd
from model import (
    VIOLATION_SORT_BY,
    SORT,
    AbstractAnimalRepository,
    AbstractViolationRepository,
    AbstractViolationTypeRepository,
    AnimalQuery,
    ViolationQuery,
    Violation,
)
from pydantic import BaseModel, Extra


class ViolationData(BaseModel):
    id: str
    animal_id: str
    animal_name: str
    animal_description: str
    is_animal_deactivated: bool
    photo_url: str
    violation_type_name: str
    judge: str
    probability: float
    is_effective: bool
    is_administrator_checked: bool
    animal_created_at: datetime
    updated_at: datetime

    class Config:
        extra = Extra.forbid


class BaseService(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)


class AbstractAnimalService(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        violation_repository: AbstractViolationRepository,
    ):
        self.animal_repository = animal_repository
        self.violation_repository = violation_repository

    @abstractmethod
    def get_animals(
        self,
        ids: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def activate(
        self,
        animal_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def deactivate(
        self,
        animal_id: str,
    ):
        raise NotImplementedError


class AnimalService(BaseService, AbstractAnimalService):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        violation_repository: AbstractViolationRepository,
    ):
        BaseService.__init__(self)
        AbstractAnimalService.__init__(
            self,
            animal_repository=animal_repository,
            violation_repository=violation_repository,
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

    def activate(
        self,
        animal_id: str,
    ):
        violation_query = ViolationQuery(
            animal_id=animal_id,
            is_effective=True,
        )
        violations = self.violation_repository.select(
            violation_query=violation_query,
            sort_by=VIOLATION_SORT_BY.UPDATED_AT.value,
            sort=SORT.ASC.value,
        )
        if len(violations) > 0:
            return

        self.animal_repository.update_deactivated(
            animal_id=animal_id,
            deactivated=False,
        )

    def deactivate(
        self,
        animal_id: str,
    ):
        self.animal_repository.update_deactivated(
            animal_id=animal_id,
            deactivated=True,
        )


class AbstractViolationTypeService(ABC):
    def __init__(
        self,
        violation_type_repository: AbstractViolationTypeRepository,
    ):
        self.violation_type_repository = violation_type_repository

    @abstractmethod
    def get_violation_types(self) -> Dict[str, str]:
        raise NotImplementedError


class ViolationTypeService(BaseService, AbstractViolationTypeService):
    def __init__(
        self,
        violation_type_repository: AbstractViolationTypeRepository,
    ):
        BaseService.__init__(self)
        AbstractViolationTypeService.__init__(
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


class AbstractViolationService(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        violation_repository: AbstractViolationRepository,
    ):
        self.animal_repository = animal_repository
        self.violation_repository = violation_repository

    @abstractmethod
    def list_violation_sort_by(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def list_sort(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def list_days_from(self) -> List[int]:
        raise NotImplementedError

    @abstractmethod
    def list_aggregate_violation(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_raw_violations(
        self,
        ids: Optional[List[str]] = None,
        animal_id: Optional[str] = None,
        violation_type_id: Optional[str] = None,
        judge: Optional[str] = None,
        is_effective: Optional[bool] = None,
        is_administrator_checked: Optional[bool] = None,
        animal_days_from: Optional[int] = None,
        days_from: int = DAYS_FROM.ONE_WEEK.value,
        sort_by: str = VIOLATION_SORT_BY.ID.value,
        sort: str = SORT.ASC.value,
    ) -> List[ViolationData]:
        raise NotImplementedError

    @abstractmethod
    def get_violations(
        self,
        ids: Optional[List[str]] = None,
        animal_id: Optional[str] = None,
        violation_type_id: Optional[str] = None,
        judge: Optional[str] = None,
        is_effective: Optional[bool] = None,
        is_administrator_checked: Optional[bool] = None,
        animal_days_from: Optional[int] = None,
        days_from: int = DAYS_FROM.ONE_WEEK.value,
        sort_by: str = VIOLATION_SORT_BY.ID.value,
        sort: str = SORT.ASC.value,
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def aggregate_violations(
        self,
        violation_df: pd.DataFrame,
        column: str = AGGREGATE_VIOLATION.UPDATED_AT.value,
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def register_admin_check(
        self,
        violation_id: str,
        is_violation: bool,
    ):
        raise NotImplementedError


class ViolationService(BaseService, AbstractViolationService):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        violation_repository: AbstractViolationRepository,
    ):
        BaseService.__init__(self)
        AbstractViolationService.__init__(
            self,
            animal_repository=animal_repository,
            violation_repository=violation_repository,
        )

    def list_violation_sort_by(self) -> List[str]:
        return VIOLATION_SORT_BY.get_list()

    def list_sort(self) -> List[str]:
        return SORT.get_list()

    def list_days_from(self) -> List[int]:
        return DAYS_FROM.get_list()

    def list_aggregate_violation(self) -> List[str]:
        return AGGREGATE_VIOLATION.get_list()

    def __get_violations(
        self,
        ids: Optional[List[str]] = None,
        animal_id: Optional[str] = None,
        violation_type_id: Optional[str] = None,
        judge: Optional[str] = None,
        is_effective: Optional[bool] = None,
        is_administrator_checked: Optional[bool] = None,
        animal_days_from: Optional[int] = None,
        days_from: int = DAYS_FROM.ONE_WEEK.value,
        sort_by: str = VIOLATION_SORT_BY.ID.value,
        sort: str = SORT.ASC.value,
    ) -> List[Violation]:
        query = ViolationQuery(
            ids=ids,
            animal_id=animal_id,
            violation_type_id=violation_type_id,
            judge=judge,
            is_effective=is_effective,
            is_administrator_checked=is_administrator_checked,
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
                sort=sort,
                limit=limit,
                offset=offset,
            )
            if len(_violations) == 0:
                break
            violations.extend(_violations)
            offset += limit
        return violations

    def get_raw_violations(
        self,
        ids: Optional[List[str]] = None,
        animal_id: Optional[str] = None,
        violation_type_id: Optional[str] = None,
        judge: Optional[str] = None,
        is_effective: Optional[bool] = None,
        is_administrator_checked: Optional[bool] = None,
        animal_days_from: Optional[int] = None,
        days_from: int = DAYS_FROM.ONE_WEEK.value,
        sort_by: str = VIOLATION_SORT_BY.ID.value,
        sort: str = SORT.ASC.value,
    ) -> List[ViolationData]:
        violations = self.__get_violations(
            ids=ids,
            animal_id=animal_id,
            violation_type_id=violation_type_id,
            judge=judge,
            is_effective=is_effective,
            is_administrator_checked=is_administrator_checked,
            animal_days_from=animal_days_from,
            days_from=days_from,
            sort_by=sort_by,
            sort=sort,
        )
        violation_data = [
            ViolationData(
                id=v.id,
                animal_id=v.animal_id,
                animal_name=v.animal_name,
                animal_description=v.animal_description,
                is_animal_deactivated=v.is_animal_deactivated,
                photo_url=v.photo_url,
                violation_type_name=v.violation_type_name,
                judge=v.judge,
                probability=v.probability,
                is_effective=v.is_effective,
                is_administrator_checked=v.is_administrator_checked,
                animal_created_at=v.animal_created_at,
                updated_at=v.updated_at,
            )
            for v in violations
        ]
        return violation_data

    def get_violations(
        self,
        ids: Optional[List[str]] = None,
        animal_id: Optional[str] = None,
        violation_type_id: Optional[str] = None,
        judge: Optional[str] = None,
        is_effective: Optional[bool] = None,
        is_administrator_checked: Optional[bool] = None,
        animal_days_from: Optional[int] = None,
        days_from: int = DAYS_FROM.ONE_WEEK.value,
        sort_by: str = VIOLATION_SORT_BY.ID.value,
        sort: str = SORT.ASC.value,
    ) -> pd.DataFrame:
        violations = self.__get_violations(
            ids=ids,
            animal_id=animal_id,
            violation_type_id=violation_type_id,
            judge=judge,
            is_effective=is_effective,
            is_administrator_checked=is_administrator_checked,
            animal_days_from=animal_days_from,
            days_from=days_from,
            sort_by=sort_by,
            sort=sort,
        )
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

    def register_admin_check(
        self,
        violation_id: str,
        is_violation: bool,
    ):
        self.violation_repository.update_is_effective(
            violation_id=violation_id,
            is_effective=is_violation,
        )
        self.violation_repository.update_is_administrator_checked(violation_id=violation_id)
