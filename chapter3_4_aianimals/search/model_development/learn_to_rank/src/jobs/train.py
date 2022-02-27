from typing import List, Optional
import numpy as np
from pydantic import BaseModel
from src.middleware.logger import configure_logger
from src.models.base_model import BaseLearnToRankModel

logger = configure_logger(name=__name__)


class Artifact(BaseModel):
    model_file_path: Optional[str]
    onnx_file_path: Optional[str]


class Trainer(object):
    def __init__(self):
        pass

    def train(
        self,
        model: BaseLearnToRankModel,
        model_save_file_path: str,
        x_train: List[List[float]],
        y_train: List[int],
        x_test: List[List[float]],
        y_test: List[int],
        q_train: Optional[List[int]] = None,
        q_test: Optional[List[int]] = None,
    ) -> Artifact:
        logger.info(
            f"""
data to train
x_train: {len(x_train)}
y_train: {len(y_train)}
x_test: {len(x_test)}
y_test: {len(y_test)}
q_train: {sum(q_train) if q_train is not None else None}
q_test: {sum(q_test) if q_test is not None else None}
        """
        )

        model.train(
            x_train=np.array(x_train),
            y_train=np.array(y_train),
            x_test=np.array(x_test),
            y_test=np.array(y_test),
            q_train=q_train,
            q_test=q_test,
        )

        model_file_path = model.save(file_path=model_save_file_path)
        onnx_file_path = model.save_onnx(
            file_path=model_save_file_path,
            batch_size=40,
            feature_size=np.array(x_train).shape[1],
        )
        return Artifact(
            model_file_path=model_file_path,
            onnx_file_path=onnx_file_path,
        )
