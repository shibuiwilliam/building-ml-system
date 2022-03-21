import os
import shutil
from typing import List

import mlflow
from mlflow.tracking import MlflowClient
from src.configurations import Configurations
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


def download_model(
    mlflow_client: MlflowClient,
    run_id: str,
    save_as: str,
) -> str:
    logger.info(f"target download: {save_as}")
    model_path = mlflow_client.download_artifacts(
        run_id=run_id,
        path=save_as,
    )
    path = os.path.join(model_path, os.listdir(model_path)[0])
    if path.endswith(".zip"):
        directory = os.path.dirname(path)
        basename = os.path.basename(path)
        filename, _ = os.path.splitext(basename)
        _path = os.path.join(directory, filename)
        shutil.unpack_archive(
            filename=path,
            extract_dir=_path,
        )
        path = _path
    logger.info(f"downloaded {path}")
    return path


def download_models(
    mlflow_client: MlflowClient,
    run_id: str,
    save_as_list: List[str],
) -> List[str]:
    logger.info(f"target downloads: {save_as_list}")
    model_paths = []
    for save_as in save_as_list:
        model_path = download_model(
            mlflow_client=mlflow_client,
            run_id=run_id,
            save_as=save_as,
        )
        model_paths.append(model_path)
    logger.info(f"downloaded {len(model_paths)} models")
    return model_paths


def main():
    logger.info("download model...")

    try:
        mlflow_client = MlflowClient()
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
        mlflow.set_experiment(experiment_id=Configurations.mlflow_experiment_id)
        run = mlflow_client.get_run(run_id=Configurations.mlflow_run_id)

        logger.info(f"target mlflow run: {run}")

        model_paths = download_models(
            mlflow_client=mlflow_client,
            run_id=run.info.run_id,
            save_as_list=Configurations.target_artifacts,
        )
        for model_path in model_paths:
            basename = os.path.basename(model_path)
            target_path = os.path.join(Configurations.target_directory, basename)
            moved_to = shutil.move(model_path, target_path)
            logger.info(f"moved to {moved_to}")
            logger.info(
                f"files {[os.path.join(Configurations.target_directory, f) for f in os.listdir(Configurations.target_directory)]}"
            )

        logger.info("done downloading model...")

    except Exception as e:
        logger.error(f"failed downloading model: {e}")


if __name__ == "__main__":
    main()
