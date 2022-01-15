from typing import List

import tensorflow as tf
from pydantic import BaseModel
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow_similarity.architectures import EfficientNetSim
from tensorflow_similarity.losses import CircleLoss
from tensorflow_similarity.samplers import Sampler


class InputShape(BaseModel):
    h: int
    w: int
    d: int


class EfficientNetSimilarityModel(object):
    def __init__(
        self,
        input_shape: InputShape = InputShape(
            h=224,
            w=224,
            d=3,
        ),
        embedding_size: int = 128,
        variant: str = "B0",
        weights: str = "imagenet",
    ):
        self.input_shape = tuple(
            [
                input_shape.h,
                input_shape.w,
                input_shape.d,
            ]
        )
        self.embedding_size = embedding_size
        self.variant = variant
        self.weights = weights

    def build_model(self):
        self.model = EfficientNetSim(
            self.input_shape,
            self.embedding_size,
            augmentation=None,
            variant=self.variant,
            weights=self.weights,
        )

    def train(
        self,
        train_data: Sampler,
        test_data: Sampler,
        epochs: int = 10,
        learning_rate: float = 0.0001,
        gamma: int = 256,
        steps_per_epoch: int = 100,
        validation_steps: int = 50,
        callbacks: List[Callback] = [],
    ):
        loss = CircleLoss(gamma=gamma)
        self.model.compile(
            optimizer=Adam(learning_rate),
            loss=loss,
        )
        self.model.fit(
            train_data,
            epochs=epochs,
            steps_per_epoch=steps_per_epoch,
            validation_data=test_data,
            validation_steps=validation_steps,
            callbacks=callbacks,
        )

    def save(
        self,
        path: str,
    ):
        self.model.save(path)

    def load(
        self,
        path: str,
    ):
        self.model = load_model(path)

    def reset_index(self):
        self.model.reset_index()

    def index(
        self,
        x: tf.Tensor,
        y: tf.Tensor,
        data: tf.Tensor,
        reset_index: bool = False,
    ):
        if reset_index:
            self.reset_index()
        self.model.index(
            x,
            y,
            data=data,
        )
