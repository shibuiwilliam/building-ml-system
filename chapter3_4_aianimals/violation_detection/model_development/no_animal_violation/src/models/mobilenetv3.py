import os
from datetime import datetime
from typing import Any, List

import tensorflow as tf
import tensorflow_hub as hub
from nptyping import NDArray
from sklearn.metrics import accuracy_score, precision_score, recall_score
from src.model.abstract_model import AbstractModel, Evaluation
from src.utils.logger import configure_logger
from tensorflow import keras

logger = configure_logger(__name__)


class MobilenetV3(AbstractModel):
    def __init__(
        self,
        num_classes: int = 2,
        tfhub_url: str = "https://tfhub.dev/google/imagenet/mobilenet_v3_large_100_224/classification/5",
    ):
        super().__init__(num_classes=num_classes)
        self.tfhub_url = tfhub_url
        self.hwd = (224, 224, 3)

    def define_base_model(
        self,
        trainable: bool = True,
        lr: float = 0.0005,
        loss: str = "categorical_crossentropy",
        metrics: List[str] = ["acc"],
    ):
        self.model = keras.Sequential(
            [
                hub.KerasLayer(
                    self.tfhub_url,
                    trainable=trainable,
                ),
                tf.keras.layers.Dense(
                    self.num_classes,
                    activation="softmax",
                ),
            ],
        )
        self.model.build([None, *self.hwd])
        self.model.compile(
            optimizer=keras.optimizers.Adam(lr=lr),
            loss=loss,
            metrics=metrics,
        )

    def define_augmentation(
        self,
        rotation_range: int = 10,
        horizontal_flip: bool = True,
        height_shift_range: float = 0.2,
        width_shift_range: float = 0.2,
        zoom_range: float = 0.2,
        channel_shift_range: float = 0.2,
    ):
        self.train_datagen = keras.preprocessing.image.ImageDataGenerator(
            rotation_range=rotation_range,
            horizontal_flip=horizontal_flip,
            height_shift_range=height_shift_range,
            width_shift_range=width_shift_range,
            zoom_range=zoom_range,
            channel_shift_range=channel_shift_range,
        )
        self.test_datagen = keras.preprocessing.image.ImageDataGenerator()

    def train(
        self,
        x_train: NDArray[(Any, 224, 224, 3), float],
        y_train: NDArray[(Any, 2), int],
        x_test: NDArray[(Any, 224, 224, 3), float],
        y_test: NDArray[(Any, 2), int],
        artifact_path: str,
        batch_size: int = 32,
        epochs: int = 100,
        checkpoint: bool = True,
        early_stopping: bool = True,
        tensorboard: bool = True,
    ):
        callbacks: List[keras.callbacks] = []
        if checkpoint:
            checkpoint_filepath = os.path.join(artifact_path, "checkpoint")
            callbacks.append(
                keras.callbacks.ModelCheckpoint(
                    checkpoint_filepath,
                    monitor="val_loss",
                    save_best_only=True,
                    save_weights_only=True,
                )
            )
        if early_stopping:
            callbacks.append(
                keras.callbacks.EarlyStopping(
                    monitor="val_loss",
                    patience=2,
                    verbose=1,
                    mode="auto",
                    restore_best_weights=True,
                )
            )
        if tensorboard:
            log_dir = os.path.join(artifact_path, datetime.now().strftime("%Y%m%d_%H%M%S"))
            callbacks.append(
                keras.callbacks.TensorBoard(
                    log_dir=log_dir,
                    histogram_freq=1,
                )
            )

        train_generator = self.train_datagen.flow(
            x_train,
            y_train,
            batch_size=batch_size,
            seed=1234,
        )
        test_generator = self.test_datagen.flow(
            x_test,
            y_test,
            batch_size=batch_size,
            seed=1234,
        )
        history = self.model.fit(
            train_generator,
            validation_data=test_generator,
            validation_steps=1,
            steps_per_epoch=len(x_train) / batch_size,
            epochs=epochs,
            callbacks=callbacks,
        )
        logger.info(f"train history: {history}")

    def evaluate(
        self,
        x: NDArray[(Any, 224, 224, 3), float],
        y: NDArray[(Any, 2), int],
        threshold: float = 0.5,
    ) -> Evaluation:
        predictions = self.model.predict(x).tolist()
        y_pred = [1 if p[1] >= threshold else 0 for p in predictions]
        y_true = y.argmax(axis=1).tolist()
        accuracy = accuracy_score(y_true, y_pred)
        positive_precision = precision_score(y_true, y_pred, pos_label=1)
        positive_recall = recall_score(y_true, y_pred, pos_label=1)
        negative_precision = precision_score(y_true, y_pred, pos_label=0)
        negative_recall = recall_score(y_true, y_pred, pos_label=0)
        evaluation = Evaluation(
            threshold=threshold,
            accuracy=accuracy,
            positive_precision=positive_precision,
            positive_recall=positive_recall,
            negative_precision=negative_precision,
            negative_recall=negative_recall,
        )
        logger.info(f"evaluated: {evaluation}")
        return evaluation

    def predict(
        self,
        x: NDArray[(Any, 224, 224, 3), float],
    ) -> NDArray[(Any, 2), float]:
        predictions = self.model.predict(x)
        return predictions

    def save_as_saved_model(
        self,
        save_dir: str,
        version: int = 0,
    ) -> str:
        saved_model = os.path.join(save_dir, "raindrop_mobilenetv3", str(version))
        keras.backend.set_learning_phase(0)
        tf.saved_model.save(self.model, saved_model)
        logger.info(f"saved model: {saved_model}")
        return saved_model

    def save_as_tflite(
        self,
        save_path: str,
    ) -> str:
        dirname = os.path.dirname(save_path)
        if not os.path.exists(dirname):
            os.makedirs(
                dirname,
                exist_ok=True,
            )
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        tflite_model = converter.convert()
        with open(save_path, "wb") as f:
            f.write(tflite_model)
        return save_path
