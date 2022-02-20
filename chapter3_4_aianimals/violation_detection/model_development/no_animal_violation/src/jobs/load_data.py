from typing import Any, List, Tuple

import numpy as np
from nptyping import NDArray
from PIL import Image
from src.dataset.schema import ImageShape, TrainTestDataset
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


def load_image_and_label(
    filepath: str,
    label: int,
    image_shape: ImageShape,
) -> Tuple[NDArray[(Any, Any, Any, Any), float], int]:
    img = Image.open(filepath).convert(image_shape.color)
    img = img.resize((image_shape.height, image_shape.width))
    arr = np.array(img) / 255.0
    return arr, label


def load_images_and_labels(
    negative_filepaths: List[str],
    positive_filepaths: List[str],
    image_shape: ImageShape,
) -> Tuple[NDArray[(Any, Any, Any, Any), float], NDArray[(Any, 2), int],]:
    x = np.zeros(
        (
            len(negative_filepaths) + len(positive_filepaths),
            image_shape.height,
            image_shape.width,
            image_shape.depth,
        )
    ).astype(np.float32)
    y = np.zeros(
        (
            len(negative_filepaths) + len(positive_filepaths),
            2,
        )
    ).astype(np.uint8)

    i = 0
    for f in negative_filepaths:
        arr, label = load_image_and_label(
            filepath=f,
            label=0,
            image_shape=image_shape,
        )
        x[i] = arr
        y[i] = label
        i += 1
        if i % 100 == 0:
            logger.info(f"loaded: {i} images")
    for f in positive_filepaths:
        arr, label = load_image_and_label(
            filepath=f,
            label=1,
            image_shape=image_shape,
        )
        x[i] = arr
        y[i] = label
        i += 1
        if i % 100 == 0:
            logger.info(f"loaded: {i} images")
    return x, y


def load_dataset(
    dataset: TrainTestDataset,
    image_shape: ImageShape,
) -> Tuple[
    Tuple[
        NDArray[(Any, Any, Any, Any), float],
        NDArray[(Any, 2), int],
    ],
    Tuple[
        NDArray[(Any, Any, Any, Any), float],
        NDArray[(Any, 2), int],
    ],
]:
    logger.info("start loading image")
    x_train, y_train = load_images_and_labels(
        negative_filepaths=dataset.train_dataset.negative_filepaths,
        positive_filepaths=dataset.train_dataset.positive_filepaths,
        image_shape=image_shape,
    )
    x_test, y_test = load_images_and_labels(
        negative_filepaths=dataset.test_dataset.negative_filepaths,
        positive_filepaths=dataset.test_dataset.positive_filepaths,
        image_shape=image_shape,
    )
    logger.info(
        f"""
Loaded dataset:
    Train: {x_train.shape}
        Negatives: {len(dataset.train_dataset.negative_filepaths)}
        Positives: {len(dataset.train_dataset.positive_filepaths)}
    Test: {x_test.shape}
        Negatives: {len(dataset.test_dataset.negative_filepaths)}
        Positives: {len(dataset.test_dataset.positive_filepaths)}
    """
    )
    logger.info("done loading image")
    return (x_train, y_train), (x_test, y_test)
