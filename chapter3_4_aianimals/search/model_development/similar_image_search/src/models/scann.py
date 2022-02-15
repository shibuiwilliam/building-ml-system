from typing import List

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_recommenders as tfrs
from sqlalchemy import false
from src.dataset.schema import Dataset
from src.middleware.logger import configure_logger
from tensorflow import keras

logger = configure_logger(__name__)


class Scann(keras.Model):
    def __init__(
        self,
        feature_extraction,
        model,
    ):
        super().__init__(self)
        self.feature_extraction = feature_extraction
        self.model = model

    @tf.function(
        input_signature=[
            tf.TensorSpec(
                shape=[None, 224, 224, 3],
                dtype=tf.float32,
                name="image",
            ),
            tf.TensorSpec(
                shape=[1],
                dtype=tf.int32,
                name="k",
            ),
        ]
    )
    def serving_fn(
        self,
        input_img: List[float],
        k: int,
    ) -> tf.Tensor:
        feature = self.feature_extraction(input_img)
        return self.model(feature, k=k)

    def save(
        self,
        export_path: str = "./saved_model/scann/0",
    ):
        signatures = {"serving_default": self.serving_fn}
        keras.backend.set_learning_phase(0)
        tf.saved_model.save(self, export_path, signatures=signatures)


class ScannModel(object):
    def __init__(
        self,
        tfhub_url: str = "https://tfhub.dev/google/imagenet/mobilenet_v3_large_100_224/classification/5",
        height: int = 224,
        width: int = 224,
    ):
        self.tfhub_url = tfhub_url
        self.hwd = (height, width, 3)

    def __define_feature_extraction(self):
        self.feature_extraction = keras.Sequential(
            [
                hub.KerasLayer(
                    self.tfhub_url,
                    trainable=false,
                ),
            ],
        )
        self.feature_extraction.build([None, *self.hwd])

    def __make_embedding_data(
        self,
        dataset: Dataset,
        batch_size: int = 32,
    ):
        id_data = tf.data.Dataset.from_tensor_slices(dataset.ids)
        image_data = tf.data.Dataset.from_tensor_slices(dataset.data)
        self.x_train_embedding = tf.data.Dataset.zip(
            (
                id_data.batch(batch_size),
                image_data.batch(batch_size).map(self.feature_extraction),
            )
        )

    def __define_similarity_search_model(
        self,
        num_leaves: int = 1000,
        num_leaves_to_search: int = 100,
        num_reordering_candidates: int = 100,
    ):
        self.model = tfrs.layers.factorized_top_k.ScaNN(
            num_leaves=num_leaves,
            num_leaves_to_search=num_leaves_to_search,
            num_reordering_candidates=num_reordering_candidates,
        )

    def make_similarity_search_model(
        self,
        dataset: Dataset,
        batch_size: int = 32,
        num_leaves: int = 1000,
        num_leaves_to_search: int = 100,
        num_reordering_candidates: int = 100,
    ):
        self.__define_feature_extraction()
        self.__make_embedding_data(dataset=dataset, batch_size=batch_size)
        self.__define_similarity_search_model(
            num_leaves=num_leaves,
            num_leaves_to_search=num_leaves_to_search,
            num_reordering_candidates=num_reordering_candidates,
        )
        self.scann = Scann(
            feature_extraction=self.feature_extraction,
            model=self.model,
        )

    def save_as_saved_model(
        self,
        saved_model: str = "./saved_model/scann/0",
    ) -> str:
        self.scann.save(export_path=saved_model)
        logger.info(f"saved model: {saved_model}")
        return saved_model
