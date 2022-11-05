from typing import Dict

from src.schema.base import Base


def model_to_dict(row: Base) -> Dict:
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d
