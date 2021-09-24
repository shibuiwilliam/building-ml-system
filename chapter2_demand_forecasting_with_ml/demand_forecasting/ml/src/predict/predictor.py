import dataclasses
from abc import ABC, abstractmethod
from typing import List, Union

import numpy as np
import onnxruntime
import pandas as pd
from sklearn.pipeline import FeatureUnion, Pipeline
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


@dataclasses.dataclass(frozen=True)
class Predictions(object):
    preprocessed_data: pd.DataFrame
    predictions: np.ndarray


class BasePredictor(ABC):
    def __init__(
        self,
        file_path: str,
        preprocess_pipeline: Union[FeatureUnion, Pipeline],
    ):
        self.file_path = file_path
        self.preprocess_pipeline = preprocess_pipeline
        self.predictor = None

    @abstractmethod
    def describe(self):
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        data: pd.DataFrame,
    ) -> Predictions:
        raise NotImplementedError


class OnnxPredictor(BasePredictor):
    def __init__(
        self,
        file_path: str,
        preprocess_pipeline: Union[FeatureUnion, Pipeline],
    ):
        super().__init__(
            file_path=file_path,
            preprocess_pipeline=preprocess_pipeline,
        )

        self.predictor: onnxruntime.InferenceSession = None

        self.input_name: str = ""
        self.input_type: str = ""
        self.input_shape: List = []
        self.output_name: str = ""
        self.output_type: str = ""
        self.output_shape: List = []

        self.__load_model()

    def __load_model(self):
        logger.info(f"load model: {self.file_path}")
        self.predictor = onnxruntime.InferenceSession(self.file_path)

        self.input_name = self.predictor.get_inputs()[0].name
        self.input_type = self.predictor.get_inputs()[0].type
        self.input_shape = self.predictor.get_inputs()[0].shape
        self.output_name = self.predictor.get_outputs()[0].name
        self.output_type = self.predictor.get_outputs()[0].type
        self.output_shape = self.predictor.get_outputs()[0].shape

    def describe(self):
        for i, session_input in enumerate(self.predictor.get_inputs()):
            logger.info(f"input {i} {session_input}")
        for i, session_output in enumerate(self.predictor.get_outputs()):
            logger.info(f"output {i} {session_output}")

    def predict(
        self,
        data: pd.DataFrame,
    ) -> Predictions:
        logger.info(f"run prediction for {data.shape} data")
        preprocessed_data = self.preprocess_pipeline.transform(x=data)
        preprocessed_df = self.preprocess_pipeline.to_dataframe(
            base_dataframe=data,
            x=preprocessed_data,
        )
        x_test = preprocessed_df.drop(["date", "store", "item"], axis=1)
        predictions = self.predictor.run(
            [self.output_name],
            {self.input_name: x_test.values.astype("float64")},
        )
        logger.info(f"done prediction for {data.shape} data")
        return Predictions(
            preprocessed_data=preprocessed_df,
            predictions=predictions[0].reshape(1, -1)[0],
        )
