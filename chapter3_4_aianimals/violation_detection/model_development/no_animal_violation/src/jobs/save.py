from src.middleware.logger import configure_logger
from src.models.abstract_model import AbstractModel

logger = configure_logger(__name__)


def save_as_saved_model(
    model: AbstractModel,
    save_dir: str,
    version: int = 0,
) -> str:
    return model.save_as_saved_model(
        save_dir=save_dir,
        version=version,
    )


def save_as_tflite(
    model: AbstractModel,
    save_path: str,
) -> str:
    return model.save_as_tflite(save_path=save_path)
