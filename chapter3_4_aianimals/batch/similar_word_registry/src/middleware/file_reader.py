import csv
from typing import Dict, List, Optional

from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


def read_text_file(file_path: str) -> str:
    file_content = ""
    with open(file_path, "r") as f:
        for line in f:
            file_content += line
    return file_content


def read_csv_to_list(
    csv_file: str,
    header: Optional[List[str]] = None,
    is_first_line_header: bool = True,
) -> List[Dict]:
    logger.info(f"read csv {csv_file}")
    csv_List: List[Dict] = []
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        if is_first_line_header or header is None:
            header = next(reader)
        logger.info(f"header: {header}")
        for r in reader:
            row = {}
            for _h, _r in zip(header, r):
                row[_h] = _r
            csv_List.append(row)
    return csv_List
