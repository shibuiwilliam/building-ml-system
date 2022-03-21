import json
import os
import shutil
from datetime import datetime

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
    experiment_name = os.getenv("MLFLOW_EXPERIMENT", "similar_image_search")
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"{cfg.task_name}_{now}"

    logger.info(f"current working directory: {cwd}")
    logger.info(f"experiment_name: {experiment_name}")
    logger.info(f"run_name: {run_name}")

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
    mlflow.set_experiment(experiment_name=experiment_name)
    with mlflow.start_run(run_name=run_name) as run:
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
        scann_model.save_as_saved_model(saved_model="/opt/outputs/saved_model/similar_image_search/0")
        shutil.make_archive(
            "saved_model",
            format="zip",
            root_dir="/opt/outputs",
        )
        saved_model_zip = shutil.move("./saved_model.zip", "/opt/outputs/saved_model.zip")

        mlflow.log_artifact(saved_model_zip, "saved_model")
        mlflow.log_artifacts(os.path.join(cwd, ".hydra/"), "hydra")
        mlflow.log_artifact(os.path.join(cwd, "main.log"))
        mlflow.log_params(cfg.model)
        mlflow.log_params(cfg.input)

        with open("/tmp/output.json", "w") as f:
            json.dump(
                dict(
                    mlflow_experiment_id=run.info.experiment_id,
                    mlflow_run_id=run.info.run_id,
                ),
                f,
            )


if __name__ == "__main__":
    main()
