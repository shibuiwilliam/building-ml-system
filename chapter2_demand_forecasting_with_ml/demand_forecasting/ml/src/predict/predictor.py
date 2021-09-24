from abc import ABC, abstractmethod
from typing import List, Union

import numpy as np
import onnxruntime
import pandas as pd
from sklearn.pipeline import FeatureUnion, Pipeline
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


class BasePredictor(ABC):
    def __init__(
        self,
        preprocess_pipeline: Union[FeatureUnion, Pipeline],
    ):
        self.preprocess_pipeline = preprocess_pipeline
        self.predictor = None

    @abstractmethod
    def load_model(self, file_path: str):
        raise NotImplementedError

    @abstractmethod
    def describe(self):
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        data: pd.DataFrame,
    ) -> np.ndarray:
        raise NotImplementedError


class OnnxPredictor(BasePredictor):
    def __init__(
        self,
        preprocess_pipeline: Union[FeatureUnion, Pipeline],
    ):
        super().__init__(preprocess_pipeline=preprocess_pipeline)
        self.predictor: onnxruntime.InferenceSession = None

        self.input_name: str = ""
        self.input_type: str = ""
        self.input_shape: List = []
        self.output_name: str = ""
        self.output_type: str = ""
        self.output_shape: List = []

    def load_model(self, file_path: str):
        self.predictor = onnxruntime.InferenceSession(file_path)

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
    ) -> np.ndarray:
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
        return predictions[0].reshape(1, -1)[0]
