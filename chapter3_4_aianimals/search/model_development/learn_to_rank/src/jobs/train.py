from typing import List, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel
from src.middleware.logger import configure_logger
from src.models.base_model import BaseLearnToRankModel
from src.models.preprocess import Preprocess

logger = configure_logger(name=__name__)


class Artifact(BaseModel):
    preprocess_file_path: Optional[str]
    model_file_path: Optional[str]
    onnx_file_path: Optional[str]


class Trainer(object):
    def __init__(self):
        pass

    def train(
        self,
        pipeline: Preprocess,
        model: BaseLearnToRankModel,
        preprocess_save_file_path: str,
        model_save_file_path: str,
        x_train: pd.DataFrame,
        y_train: np.ndarray,
        x_test: Optional[pd.DataFrame] = None,
        y_test: Optional[np.ndarray] = None,
        q_train: Optional[List[int]] = None,
        q_test: Optional[List[int]] = None,
    ):
        _x_train = pipeline.fit_transform(x_train)
        _x_test = pipeline.transform(x_test)
        model.train(
            x_train=_x_train,
            y_train=y_train,
            x_test=_x_test,
            y_test=y_test,
            q_train=q_train,
            q_test=q_test,
        )

        preprocess_file_path = pipeline.save(file_path=preprocess_save_file_path)
        model_file_path = model.save(file_path=model_save_file_path)
        onnx_file_path = model.save_onnx(
            file_path=model_save_file_path,
            batch_size=50,
            feature_size=_x_train.shape[1],
        )
        return Artifact(
            preprocess_file_path=preprocess_file_path,
            model_file_path=model_file_path,
            onnx_file_path=onnx_file_path,
        )
