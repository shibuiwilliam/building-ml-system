from typing import Any, List

from nptyping import NDArray
from src.middleware.logger import configure_logger
from src.models.abstract_model import AbstractModel, Evaluation
from src.models.mobilenetv3 import MobilenetV3

logger = configure_logger(__name__)


def initialize_model(
    num_classes: int = 2,
    tfhub_url: str = "https://tfhub.dev/google/imagenet/mobilenet_v3_large_100_224/classification/5",
    trainable: bool = True,
    lr: float = 0.0005,
    loss: str = "categorical_crossentropy",
    metrics: List[str] = ["acc"],
) -> AbstractModel:
    model = MobilenetV3(
        num_classes=num_classes,
        tfhub_url=tfhub_url,
    )
    model.define_base_model(
        trainable=trainable,
        lr=lr,
        loss=loss,
        metrics=metrics,
    )
    return model


def train_and_evaluate(
    model: AbstractModel,
    x_train: NDArray[(Any, Any, Any, 3), float],
    y_train: NDArray[(Any, 2), int],
    x_test: NDArray[(Any, Any, Any, 3), float],
    y_test: NDArray[(Any, 2), int],
    artifact_path: str,
    batch_size: int = 32,
    epochs: int = 100,
    rotation_range: int = 10,
    horizontal_flip: bool = True,
    height_shift_range: float = 0.2,
    width_shift_range: float = 0.2,
    zoom_range: float = 0.2,
    channel_shift_range: float = 0.2,
    threshold: float = 0.5,
    checkpoint: bool = True,
    early_stopping: bool = True,
    tensorboard: bool = True,
) -> Evaluation:
    model.define_augmentation(
        rotation_range=rotation_range,
        horizontal_flip=horizontal_flip,
        height_shift_range=height_shift_range,
        width_shift_range=width_shift_range,
        zoom_range=zoom_range,
        channel_shift_range=channel_shift_range,
    )
    model.train(
        x_train=x_train,
        y_train=y_train,
        x_test=x_test,
        y_test=y_test,
        artifact_path=artifact_path,
        batch_size=batch_size,
        epochs=epochs,
        checkpoint=checkpoint,
        early_stopping=early_stopping,
        tensorboard=tensorboard,
    )
    evaluation = model.evaluate(
        x=x_test,
        y=y_test,
        threshold=threshold,
    )
    return evaluation
