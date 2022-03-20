import json
import os
from datetime import datetime
from time import sleep

import cloudpickle
import hydra
import mlflow
from mlflow.tracking import MlflowClient
from omegaconf import DictConfig
from src.configurations import Configurations
from src.infrastructure.client.postgresql_database import PostgreSQLDatabase
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.infrastructure.client.redis_cache import RedisCache
from src.job.jobs import JOBS
from src.middleware.logger import configure_logger
from src.registry.container import Container
from src.service.feature_processing import (
    CategoricalVectorizer,
    DescriptionTokenizer,
    DescriptionVectorizer,
    NameTokenizer,
    NameVectorizer,
)

logger = configure_logger(__name__)


@hydra.main(
    config_path="../hydra",
    config_name=os.getenv("MODEL_CONFIG", "animal_feature"),
)
def main(cfg: DictConfig):
    logger.info(f"config: {cfg}")
    cwd = os.getcwd()

    logger.info(f"current working directory: {cwd}")

    if Configurations.job == JOBS.ANIMAL_FEATURE_INITIALIZATION_JOB.value.name:
        container = Container(
            database=PostgreSQLDatabase(),
            messaging=RabbitmqMessaging(),
            cache=RedisCache(),
            animal_category_vectorizer=CategoricalVectorizer(
                sparse=cfg.jobs.animal_category.one_hot_encoding.sparse,
                handle_unknown=cfg.jobs.animal_category.one_hot_encoding.handle_unknown,
            ),
            animal_subcategory_vectorizer=CategoricalVectorizer(
                sparse=cfg.jobs.animal_subcategory.one_hot_encoding.sparse,
                handle_unknown=cfg.jobs.animal_subcategory.one_hot_encoding.handle_unknown,
            ),
            description_tokenizer=DescriptionTokenizer(),
            name_tokenizer=NameTokenizer(),
            description_vectorizer=DescriptionVectorizer(
                max_features=cfg.jobs.description.vectorizer.max_features,
            ),
            name_vectorizer=NameVectorizer(
                max_features=cfg.jobs.name.vectorizer.max_features,
            ),
        )

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        experiment_name = Configurations.mlflow_experiment_name
        run_name = f"{cfg.task_name}_{now}"
        logger.info(f"experiment_name: {experiment_name}")
        logger.info(f"run_name: {run_name}")
        logger.info("START...")

        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
        mlflow.set_experiment(experiment_name=experiment_name)
        with mlflow.start_run(run_name=run_name) as run:
            container.animal_feature_initialization_job.run(
                mlflow_experiment_id=run.info.experiment_id,
                mlflow_run_id=run.info.run_id,
            )
            mlflow.log_artifact(os.path.join(cwd, ".hydra/config.yaml"))
            mlflow.log_artifact(os.path.join(cwd, ".hydra/hydra.yaml"))
            mlflow.log_artifact(os.path.join(cwd, ".hydra/overrides.yaml"))

            with open("/tmp/output.json", "w") as f:
                json.dump(
                    dict(
                        mlflow_experiment_id=run.info.experiment_id,
                        mlflow_run_id=run.info.run_id,
                    ),
                    f,
                )

    elif Configurations.job == JOBS.ANIMAL_FEATURE_REGISTRATION_JOB.value.name:
        if Configurations.empty_run:
            while True:
                sleep(10)
                logger.info("empty run...")
        mlflow_client = MlflowClient()
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
        experiment = mlflow_client.get_experiment_by_name(name=Configurations.mlflow_experiment_name)
        mlflow.set_experiment(experiment_id=experiment.experiment_id)
        run = mlflow_client.get_run(run_id=Configurations.mlflow_run_id)

        def download_model(
            run_id: str,
            save_as: str,
        ) -> str:
            model_path = mlflow_client.download_artifacts(
                run_id=run_id,
                path=save_as,
            )
            return os.path.join(model_path, os.listdir(model_path)[0])

        animal_category_vectorizer_path = download_model(
            run_id=run.info.run_id,
            save_as="animal_category_vectorizer",
        )
        animal_subcategory_vectorizer_path = download_model(
            run_id=run.info.run_id,
            save_as="animal_subcategory_vectorizer",
        )
        description_vectorizer_path = download_model(
            run_id=run.info.run_id,
            save_as="description_vectorizer",
        )
        name_vectorizer_path = download_model(
            run_id=run.info.run_id,
            save_as="name_vectorizer",
        )
        with open(animal_category_vectorizer_path, "rb") as f:
            animal_category_vectorizer: CategoricalVectorizer = cloudpickle.load(f)
        with open(animal_subcategory_vectorizer_path, "rb") as f:
            animal_subcategory_vectorizer: CategoricalVectorizer = cloudpickle.load(f)
        with open(description_vectorizer_path, "rb") as f:
            description_vectorizer: DescriptionTokenizer = cloudpickle.load(f)
        with open(name_vectorizer_path, "rb") as f:
            name_vectorizer: NameVectorizer = cloudpickle.load(f)
        container = Container(
            database=PostgreSQLDatabase(),
            messaging=RabbitmqMessaging(),
            cache=RedisCache(),
            animal_category_vectorizer=animal_category_vectorizer,
            animal_subcategory_vectorizer=animal_subcategory_vectorizer,
            description_tokenizer=DescriptionTokenizer(),
            name_tokenizer=NameTokenizer(),
            description_vectorizer=description_vectorizer,
            name_vectorizer=name_vectorizer,
        )
        container.animal_feature_registration_job.run(
            mlflow_experiment_id=run.info.experiment_id,
            mlflow_run_id=run.info.run_id,
        )

    else:
        raise ValueError

    logger.info("Done...")


if __name__ == "__main__":
    main()
