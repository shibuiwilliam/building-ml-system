import csv
from logging import getLogger
from typing import Any, Dict, List

logger = getLogger(name=__name__)


def read_csv_data(
    file_path: str,
) -> List[Dict[str, Any]]:
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]
    logger.debug(f"read data from {file_path}: {len(data)}")
    return data
