from logging import getLogger
from typing import Dict

from src.schema.base import Base

logger = getLogger(__name__)


class BaseRepository(object):
    def __init__(self):
        pass

    @classmethod
    def model_to_dict(cls, row: Base) -> Dict:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        return d
