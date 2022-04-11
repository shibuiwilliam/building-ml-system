import tensorflow as tf

IMAGE_SIZE = 224


class Model(tf.Module):
    def __init__(self):
        self.model = tf.keras.Sequential(
            [
                tf.keras.applications.MobileNetV3Small(
                    input_shape=(
                        IMAGE_SIZE,
                        IMAGE_SIZE,
                        3,
                    ),
                    include_top=False,
                    weights="imagenet",
                    alpha=1.0,
                    include_preprocessing=True,
                ),
                tf.keras.layers.Dense(
                    128,
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

    # The `train` function takes a batch of input images and labels.
    @tf.function(
        input_signature=[
            tf.TensorSpec(
                [
                    None,
                    IMAGE_SIZE,
                    IMAGE_SIZE,
                ],
                tf.float32,
            ),
            tf.TensorSpec(
                [
                    None,
                    2,
                ],
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
                [
                    None,
                    IMAGE_SIZE,
                    IMAGE_SIZE,
                ],
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
        return {
            "output": probabilities,
            "logits": logits,
        }

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
    model = Model()
    saved_model = "/tmp/saved_model"
    tflite_path = "/tmp/model.tflite"

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

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model)
    converter.target_spec.supported_ops = [
        tf.lite.OpsSet.TFLITE_BUILTINS,
        tf.lite.OpsSet.SELECT_TF_OPS,
    ]
    converter.experimental_enable_resource_variables = True
    tflite_model = converter.convert()
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)


if __name__ == "__main__":
    main()
