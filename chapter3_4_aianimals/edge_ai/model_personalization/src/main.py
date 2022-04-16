import os

import tensorflow as tf
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class Model(tf.Module):
    def __init__(self):
        self.model = tf.keras.Sequential(
            [
                tf.keras.layers.Flatten(
                    input_shape=(1024,),
                    name="flatten",
                ),
                tf.keras.layers.Dense(
                    256,
                    activation="relu",
                    name="dense_1",
                ),
                tf.keras.layers.Dense(
                    2,
                    activation="softmax",
                    name="softmax",
                ),
            ]
        )

        self.model.compile(
            optimizer="adam",
            loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
        )

    @tf.function(
        input_signature=[
            tf.TensorSpec(
                [None, 1024],
                tf.float32,
            ),
            tf.TensorSpec(
                [None, 2],
                tf.float32,
            ),
        ]
    )
    def train(self, x, y):
        with tf.GradientTape() as tape:
            prediction = self.model(x)
            loss = self.model.loss(
                y,
                prediction,
            )
        gradients = tape.gradient(
            loss,
            self.model.trainable_variables,
        )
        self.model.optimizer.apply_gradients(
            zip(
                gradients,
                self.model.trainable_variables,
            )
        )
        result = {"loss": loss}
        return result

    @tf.function(
        input_signature=[
            tf.TensorSpec(
                [None, 1024],
                tf.float32,
            ),
        ]
    )
    def infer(self, x):
        logits = self.model(x)
        probabilities = tf.nn.softmax(
            logits,
            axis=-1,
        )
        return {"output": probabilities}

    @tf.function(
        input_signature=[
            tf.TensorSpec(
                shape=[],
                dtype=tf.string,
            ),
        ],
    )
    def save(
        self,
        checkpoint_path: str,
    ):
        tensor_names = [weight.name for weight in self.model.weights]
        tensors_to_save = [weight.read_value() for weight in self.model.weights]
        tf.raw_ops.Save(
            filename=checkpoint_path,
            tensor_names=tensor_names,
            data=tensors_to_save,
            name="save",
        )
        return {
            "checkpoint_path": checkpoint_path,
        }

    @tf.function(
        input_signature=[
            tf.TensorSpec(
                shape=[],
                dtype=tf.string,
            )
        ]
    )
    def restore(
        self,
        checkpoint_path: str,
    ):
        restored_tensors = {}
        for var in self.model.weights:
            restored = tf.raw_ops.Restore(
                file_pattern=checkpoint_path,
                tensor_name=var.name,
                dt=var.dtype,
                name="restore",
            )
            var.assign(restored)
            restored_tensors[var.name] = restored
        return restored_tensors


def main():
    logger.info("Start...")
    model = Model()
    output_dir = "/tmp/model"
    saved_model = os.path.join(output_dir, "saved_model")
    tflite_path = os.path.join(output_dir, "model_personalization.tflite")

    tf.saved_model.save(
        model,
        saved_model,
        signatures={
            "train": model.train.get_concrete_function(),
            "infer": model.infer.get_concrete_function(),
            "save": model.save.get_concrete_function(),
            "restore": model.restore.get_concrete_function(),
        },
    )
    logger.info(f"saved to {saved_model}")

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model)
    converter.target_spec.supported_ops = [
        tf.lite.OpsSet.TFLITE_BUILTINS,
        tf.lite.OpsSet.SELECT_TF_OPS,
    ]
    converter.experimental_enable_resource_variables = True
    tflite_model = converter.convert()
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)
    logger.info(f"saved to {tflite_path}")

    logger.info("Done...")


if __name__ == "__main__":
    main()
