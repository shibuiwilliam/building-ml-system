from typing import List

from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


def read_text(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        lines = f.readlines()
    lines = [l.replace("\n", "") for l in lines]
    return lines
