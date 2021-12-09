from typing import Dict

from src.middleware.logger import configure_logger
from src.schema.base import Base

logger = configure_logger(__name__)


def model_to_dict(row: Base) -> Dict:
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d
