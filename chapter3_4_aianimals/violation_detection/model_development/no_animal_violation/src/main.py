import os

import hydra
import mlflow
from omegaconf import DictConfig
from src.dataset.schema import Dataset, ImageShape, TrainTestDataset
from src.job.load_data import load_dataset
from src.job.retrieve import download_dataset
from src.job.save import save_as_saved_model, save_as_tflite
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
    run_name = cfg.task_name
    logger.info(f"current working directory: {cwd}")
    logger.info(f"run_name: {run_name}")

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
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

        (x_train, y_train), (x_test, y_test) = load_dataset(
            dataset=train_test_dataset,
            image_shape=ImageShape(
                height=cfg.dataset.image.height,
                width=cfg.dataset.image.width,
                depth=3,
                color="RGB",
            ),
        )

        model = initialize_model(
            num_classes=2,
            tfhub_url=cfg.jobs.train.tfhub_url,
            trainable=cfg.jobs.train.train_tfhub,
            lr=cfg.jobs.train.learning_rate,
            loss=cfg.jobs.train.loss,
            metrics=cfg.jobs.train.metrics,
        )
        evaluation = train_and_evaluate(
            model=model,
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
            artifact_path=cwd,
            batch_size=cfg.jobs.train.batch_size,
            epochs=cfg.jobs.train.epochs,
            rotation_range=cfg.jobs.train.rotation_range,
            horizontal_flip=cfg.jobs.train.horizontal_flip,
            height_shift_range=cfg.jobs.train.height_shift_range,
            width_shift_range=cfg.jobs.train.width_shift_range,
            zoom_range=cfg.jobs.train.zoom_range,
            channel_shift_range=cfg.jobs.train.channel_shift_range,
            threshold=cfg.jobs.train.threshold,
            checkpoint=cfg.jobs.train.callback.checkpoint,
            early_stopping=cfg.jobs.train.callback.early_stopping,
            tensorboard=cfg.jobs.train.callback.tensorboard,
        )

        saved_model = save_as_saved_model(
            model=model,
            save_dir=os.path.join(cwd, cfg.task_name),
            version=0,
        )
        tflite = save_as_tflite(
            model=model,
            save_path=os.path.join(cwd, cfg.task_name, f"{cfg.jobs.train.model_name}.tflite"),
        )

        mlflow.log_artifact(saved_model, "saved_model")
        mlflow.log_artifact(tflite, "tflite")
        mlflow.log_artifact(os.path.join(cwd, ".hydra/config.yaml"))
        mlflow.log_artifact(os.path.join(cwd, ".hydra/hydra.yaml"))
        mlflow.log_artifact(os.path.join(cwd, ".hydra/overrides.yaml"))
        mlflow.log_artifact(os.path.join(cwd, "main.log"))
        mlflow.log_params(cfg.jobs.train)
        mlflow.log_params("image_shape", cfg.dataset.image)
        mlflow.log_metric("accuracy", evaluation.accuracy)
        mlflow.log_metric("positive_precision", evaluation.positive_precision)
        mlflow.log_metric("positive_recall", evaluation.positive_recall)
        mlflow.log_metric("negative_precision", evaluation.negative_precision)
        mlflow.log_metric("negative_recall", evaluation.negative_recall)


if __name__ == "__main__":
    main()
