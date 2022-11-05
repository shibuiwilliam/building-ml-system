from enum import Enum
from typing import List

from pydantic import BaseModel


class Job(BaseModel):
    name: str


class JOBS(Enum):
    SIMILAR_WORD_REGISTRATION_JOB = Job(name="similar_word_registration_job")

    @staticmethod
    def has_name(name: str) -> bool:
        return name in [v.value.name for v in JOBS.__members__.values()]

    @staticmethod
    def get_list() -> List[Job]:
        return [v.value for v in JOBS.__members__.values()]
