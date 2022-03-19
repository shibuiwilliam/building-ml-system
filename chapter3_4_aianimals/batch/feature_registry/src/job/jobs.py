from enum import Enum
from typing import List

from pydantic import BaseModel


class Job(BaseModel):
    name: str


class JOBS(Enum):
    INITIALIZATION_JOG = Job(name="initialization_job")
    ANIMAL_TO_SEARCH_JOB = Job(name="animal_to_search_job")
    ANIMAL_FEATURE_REGISTRATION_JOB = Job(name="animal_feature_registration_job")

    @staticmethod
    def has_name(name: str) -> bool:
        return name in [v.value.name for v in JOBS.__members__.values()]

    @staticmethod
    def get_list() -> List[Job]:
        return [v.value for v in JOBS.__members__.values()]
