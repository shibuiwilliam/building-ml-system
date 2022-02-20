import os

import hydra
import mlflow
from omegaconf import DictConfig
from src.dataset.data_manager import DBClient
from src.jobs.retrieve import download_dataset, load_images, retrieve_animals
from src.middleware.logger import configure_logger
from src.models.scann import ScannModel

logger = configure_logger(__name__)


@hydra.main(
    config_path="/opt/hydra",
    config_name="mobilenet_v3_scann",
)
def main(cfg: DictConfig):
    logger.info("start ml...")
    logger.info(f"config: {cfg}")
    cwd = os.getcwd()
    run_name = cfg.task_name

    logger.info(f"current working directory: {cwd}")
    logger.info(f"run_name: {run_name}")

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT", "similar_image_search"))
    with mlflow.start_run(run_name=run_name):
        db_client = DBClient()
        animals = retrieve_animals(db_client=db_client)
        downloaded_images = download_dataset(
            animals=animals,
            destination_directory="/opt/outputs/images",
        )
        dataset = load_images(
            images=downloaded_images,
            height=cfg.input.height,
            width=cfg.input.width,
        )

        scann_model = ScannModel(
            tfhub_url=cfg.model.tfhub_url,
            height=cfg.input.height,
            width=cfg.input.width,
        )
        scann_model.make_similarity_search_model(
            dataset=dataset,
            batch_size=cfg.model.batch_size,
            num_leaves=cfg.model.num_leaves,
            num_leaves_to_search=cfg.model.num_leaves_to_search,
            num_reordering_candidates=cfg.model.num_reordering_candidates,
        )
        saved_model = scann_model.save_as_saved_model()

        mlflow.log_artifact(saved_model, "saved_model")
        mlflow.log_artifact(os.path.join(cwd, ".hydra/config.yaml"), "hydra_config.yaml")
        mlflow.log_artifact(os.path.join(cwd, ".hydra/hydra.yaml"), "hydra_hydra.yaml")
        mlflow.log_artifact(os.path.join(cwd, ".hydra/overrides.yaml"), "hydra_overrides.yaml")
        mlflow.log_artifact(os.path.join(cwd, "main.log"))

        mlflow.log_params(cfg.model)
        mlflow.log_params(cfg.input)


if __name__ == "__main__":
    main()
