from enum import Enum
from typing import List

import pandas as pd
from src.dataset.schema import BASE_SCHEMA
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class DATA_SOURCE(Enum):
    LOCAL = "local"

    @staticmethod
    def list_values() -> List[str]:
        return [v.value for v in DATA_SOURCE.__members__.values()]

    @staticmethod
    def has_value(value: str) -> bool:
        return value in [v.value for v in DATA_SOURCE.__members__.values()]

    @staticmethod
    def value_to_enum(value: str):
        for v in DATA_SOURCE.__members__.values():
            if value == v.value:
                return v
        raise ValueError


def load_df_from_csv(file_path: str) -> pd.DataFrame:
    logger.info(f"load dataframe from {file_path}")
    df = pd.read_csv(file_path)
    df = BASE_SCHEMA.validate(df)
    return df


def save_df_to_csv(
    df: pd.DataFrame,
    file_path: str,
):
    logger.info(f"save dataframe to {file_path}")
    df.to_csv(file_path, index=False)
