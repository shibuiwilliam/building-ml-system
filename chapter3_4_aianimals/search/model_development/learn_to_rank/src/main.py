import os
from datetime import datetime

import hydra
import mlflow
from omegaconf import DictConfig
from src.dataset.data_manager import DBClient
from src.jobs.retrieve import retrieve_access_logs
from src.jobs.train import Trainer
from src.middleware.logger import configure_logger
from src.models.models import MODELS
from src.models.preprocess import Preprocess, random_split, split_by_qid

logger = configure_logger(__name__)


@hydra.main(
    config_path="/opt/hydra",
    config_name="learn_to_rank_regression",
)
def main(cfg: DictConfig):
    logger.info("start ml...")
    logger.info(f"config: {cfg}")
    cwd = os.getcwd()
    run_name = "-".join(cwd.split("/")[-2:])

    logger.info(f"current working directory: {cwd}")
    logger.info(f"run_name: {run_name}")

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
    mlflow.set_experiment(cfg.name)
    with mlflow.start_run(run_name=run_name):
        db_client = DBClient()
        train_data, target, qids = retrieve_access_logs(db_client=db_client)
        if cfg.jobs.data.split_by_qid:
            x_train, x_test, y_train, y_test, q_train, q_test = split_by_qid(
                x=train_data,
                y=target,
                qids=qids,
                test_size=0.3,
                shuffle=True,
            )
        else:
            x_train, x_test, y_train, y_test = random_split(
                x=train_data,
                y=target,
                test_size=0.3,
                shuffle=True,
            )
            q_train = None
            q_test = None

        pipeline = Preprocess()

        _model = MODELS.get_model(name=cfg.jobs.model.name)
        model = _model.model(
            early_stopping_rounds=cfg.jobs.model.params.early_stopping_rounds,
            eval_metrics=cfg.jobs.model.params.eval_metrics,
            verbose_eval=cfg.jobs.model.params.verbose_eval,
        )
        if "params" in cfg.jobs.model.keys():
            model.reset_model(params=cfg.jobs.model.params)

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        preprocess_save_file_path = os.path.join(cwd, f"{model.name}_{now}")
        model_save_file_path = os.path.join(cwd, f"{model.name}_{now}")
        trainer = Trainer()
        artifact = trainer.train(
            pipeline=pipeline,
            model=model,
            preprocess_save_file_path=preprocess_save_file_path,
            model_save_file_path=model_save_file_path,
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
            q_train=q_train,
            q_test=q_test,
        )
        mlflow.log_artifact(artifact.preprocess_file_path, "preprocess")
        mlflow.log_artifact(artifact.model_file_path, "model")
        mlflow.log_artifact(artifact.onnx_file_path, "onnx")

        mlflow.log_artifact(os.path.join(cwd, ".hydra/config.yaml"), "hydra_config.yaml")
        mlflow.log_artifact(os.path.join(cwd, ".hydra/hydra.yaml"), "hydra_hydra.yaml")
        mlflow.log_artifact(os.path.join(cwd, ".hydra/overrides.yaml"), "hydra_overrides.yaml")

        mlflow.log_param("model", model.name)
        mlflow.log_params(model.params)


if __name__ == "__main__":
    main()
