import os

import hydra
import mlflow
from omegaconf import DictConfig
from src.dataset.schema import Dataset, TrainTestDataset
from src.job.retrieve import download_dataset
from src.job.train import initialize_model, train_and_evaluate
from src.middleware.file_utils import read_text
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


@hydra.main(
    config_path="../hydra",
    config_name="mobilenet_v3",
)
def main(cfg: DictConfig):
    logger.info(f"config: {cfg}")
    cwd = os.getcwd()
    run_name = "-".join(cwd.split("/")[-2:])
    logger.info(f"current working directory: {cwd}")
    logger.info(f"run_name: {run_name}")

    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT", "no_animal_violation_detection"))
    with mlflow.start_run(run_name=run_name):
        negative_train_files = read_text(filepath=cfg.dataset.train.negative_file)
        positive_train_files = read_text(filepath=cfg.dataset.train.positive_file)
        negative_test_files = read_text(filepath=cfg.dataset.test.negative_file)
        positive_test_files = read_text(filepath=cfg.dataset.test.positive_file)

        train_test_dataset = TrainTestDataset(
            train_dataset=Dataset(
                negative_filepaths=negative_train_files,
                positive_filepaths=positive_train_files,
            ),
            test_dataset=Dataset(
                negative_filepaths=negative_test_files,
                positive_filepaths=positive_test_files,
            ),
        )
        download_dataset(
            bucket=cfg.dataset.bucket,
            filepaths=train_test_dataset.train_dataset.negative_filepaths,
            destination_directory="/opt/dataset/train/images",
        )
        download_dataset(
            bucket=cfg.dataset.bucket,
            filepaths=train_test_dataset.train_dataset.positive_filepaths,
            destination_directory="/opt/dataset/train/no_animal_images",
        )
        download_dataset(
            bucket=cfg.dataset.bucket,
            filepaths=train_test_dataset.test_dataset.negative_filepaths,
            destination_directory="/opt/dataset/test/images",
        )
        download_dataset(
            bucket=cfg.dataset.bucket,
            filepaths=train_test_dataset.test_dataset.positive_filepaths,
            destination_directory="/opt/dataset/test/no_animal_images",
        )
