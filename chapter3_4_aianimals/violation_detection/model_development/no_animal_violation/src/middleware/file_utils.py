from logging import getLogger
from typing import List

logger = getLogger(__name__)


def read_text(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        lines = f.readlines()
    lines = [l.replace("\n", "") for l in lines]
    return lines
