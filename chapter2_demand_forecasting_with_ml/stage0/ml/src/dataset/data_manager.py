import pandas as pd
from src.dataset.schema import BASE_SCHEMA
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


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
