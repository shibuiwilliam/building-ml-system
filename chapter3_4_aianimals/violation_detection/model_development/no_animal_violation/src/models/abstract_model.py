from abc import ABC, abstractmethod
from typing import Any, List, Optional

from nptyping import NDArray
from pydantic import BaseModel
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


class LabelPrediction(BaseModel):
    file_name: str
    label: int
    prediction: List[float]
    predicted_label: int


class Evaluation(BaseModel):
    label_prediction: List[LabelPrediction]
    threshold: float
    accuracy: float
    positive_precision: float
    positive_recall: float
    negative_precision: float
    negative_recall: float


class AbstractModel(ABC):
    def __init__(
        self,
        num_classes: int = 2,
    ):
        self.num_classes = num_classes

    @abstractmethod
    def define_base_model(
        self,
        trainable: bool = True,
        lr: float = 0.0005,
        loss: str = "categorical_crossentropy",
        metrics: List[str] = ["acc"],
    ):
        raise NotImplementedError

    @abstractmethod
    def define_augmentation(
        self,
        rotation_range: int = 10,
        horizontal_flip: bool = True,
        height_shift_range: float = 0.2,
        width_shift_range: float = 0.2,
        zoom_range: float = 0.2,
        channel_shift_range: float = 0.2,
    ):
        raise NotImplementedError

    @abstractmethod
    def train(
        self,
        x_train: NDArray[(Any, 299, 299, 3), float],
        y_train: NDArray[(Any, 2), int],
        x_test: NDArray[(Any, 299, 299, 3), float],
        y_test: NDArray[(Any, 2), int],
        checkpoint_filepath: str,
        pretrained_model_filepath: Optional[str] = None,
        batch_size: int = 32,
        epochs: int = 100,
    ):
        raise NotImplementedError

    @abstractmethod
    def evaluate(
        self,
        x: NDArray[(Any, 299, 299, 3), float],
        y: NDArray[(Any, 2), int],
        test_files: List[str],
        threshold: float = 0.95,
    ) -> Evaluation:
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        x: NDArray[(Any, 299, 299, 3), float],
    ) -> NDArray[(Any, 2), float]:
        raise NotImplementedError

    @abstractmethod
    def save_as_saved_model(
        self,
        save_dir: str,
        version: int = 0,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def save_as_tflite(
        self,
        save_path: str,
    ) -> str:
        raise NotImplementedError
