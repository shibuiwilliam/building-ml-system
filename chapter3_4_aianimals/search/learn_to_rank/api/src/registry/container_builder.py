import os
from logging import getLogger

import cloudpickle
import mlflow
from mlflow.tracking import MlflowClient
from onnxruntime import InferenceSession
from src.configurations import Configurations
from src.infrastructure.cache_client import RedisClient
from src.infrastructure.db_client import DBClient
from src.registry.container import Container, EmptyContainer
from src.service.learn_to_rank_service import AbstractLearnToRankService, LearnToRankService

logger = getLogger(__name__)


def download_model(
    mlflow_client: MlflowClient,
    run_id: str,
    save_as: str,
) -> str:
    model_path = mlflow_client.download_artifacts(
        run_id=run_id,
        path=save_as,
    )
    return os.path.join(model_path, os.listdir(model_path)[0])


def load_cloud_pickle(file_path: str):
    with open(file_path, "rb") as f:
        p = cloudpickle.load(f)
    logger.info(f"loaded: {file_path}")
    return p


def build_container() -> Container:
    logger.info("build container...")

    mlflow_client = MlflowClient()
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
    mlflow.set_experiment(experiment_id=Configurations.mlflow_experiment_id)
    run = mlflow_client.get_run(run_id=Configurations.mlflow_run_id)

    predictor_file_path = download_model(
        mlflow_client=mlflow_client,
        run_id=run.info.run_id,
        save_as="model",
    )
    likes_scaler_file_path = download_model(
        mlflow_client=mlflow_client,
        run_id=run.info.run_id,
        save_as="likes_scaler",
    )
    query_animal_category_id_encoder_file_path = download_model(
        mlflow_client=mlflow_client,
        run_id=run.info.run_id,
        save_as="query_animal_category_id_encoder",
    )
    query_animal_subcategory_id_encoder_file_path = download_model(
        mlflow_client=mlflow_client,
        run_id=run.info.run_id,
        save_as="query_animal_subcategory_id_encoder",
    )
    query_phrase_encoder_file_path = download_model(
        mlflow_client=mlflow_client,
        run_id=run.info.run_id,
        save_as="query_phrase_encoder",
    )

    if predictor_file_path.endswith(".pkl") or predictor_file_path.endswith(".pickle"):
        predictor = load_cloud_pickle(file_path=predictor_file_path)
    elif predictor_file_path.endswith(".onnx"):
        predictor = InferenceSession(predictor_file_path)
    else:
        raise ValueError

    likes_scaler = load_cloud_pickle(file_path=likes_scaler_file_path)
    query_animal_category_id_encoder = load_cloud_pickle(file_path=query_animal_category_id_encoder_file_path)
    query_animal_subcategory_id_encoder = load_cloud_pickle(file_path=query_animal_subcategory_id_encoder_file_path)
    query_phrase_encoder = load_cloud_pickle(file_path=query_phrase_encoder_file_path)

    learn_to_rank_service: AbstractLearnToRankService = LearnToRankService(
        preprocess_likes_scaler=likes_scaler,
        preprocess_query_animal_category_id_encoder=query_animal_category_id_encoder,
        preprocess_query_animal_subcategory_id_encoder=query_animal_subcategory_id_encoder,
        preprocess_query_phrase_encoder=query_phrase_encoder,
        predictor=predictor,
        is_onnx_predictor=Configurations.is_onnx_predictor,
        predictor_batch_size=Configurations.predictor_batch_size,
        predictor_input_name=Configurations.predictor_input_name,
        predictor_output_name=Configurations.predictor_output_name,
    )

    return Container(
        db_client=DBClient(),
        cache_client=RedisClient(),
        learn_to_rank_service=learn_to_rank_service,
    )


def build_empty_container() -> EmptyContainer:
    logger.info("build empty container...")

    return EmptyContainer()
