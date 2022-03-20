import os
import pickle
from datetime import datetime
import json

import hydra
import mlflow
from omegaconf import DictConfig
from src.dataset.data_manager import DBClient, RedisCache
from src.jobs.preprocess import Preprocess, random_split, split_by_qid
from src.jobs.retrieve import retrieve_access_logs
from src.jobs.train import Trainer
from src.middleware.logger import configure_logger
from src.models.models import MODELS
from src.models.preprocess import CategoricalVectorizer, NumericalMinMaxScaler
from src.configurations import Configurations

logger = configure_logger(__name__)


@hydra.main(
    config_path="/opt/hydra",
    config_name=os.getenv("MODEL_CONFIG", "learn_to_rank_lightgbm_regression"),
)
def main(cfg: DictConfig):
    logger.info("start ml...")
    logger.info(f"config: {cfg}")
    cwd = os.getcwd()
    experiment_name = os.getenv("MLFLOW_EXPERIMENT", "learn_to_rank")
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"{cfg.task_name}_{now}"

    logger.info(f"current working directory: {cwd}")
    logger.info(f"experiment_name: {experiment_name}")
    logger.info(f"run_name: {run_name}")
    logger.info(f"feature mlflow experiment_id: {Configurations.feature_mlflow_experiment_id}")
    logger.info(f"feature mlflow run_id: {Configurations.feature_mlflow_run_id}")

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
    mlflow.set_experiment(experiment_name=experiment_name)
    with mlflow.start_run(run_name=run_name) as run:
        db_client = DBClient()
        cache = RedisCache()
        raw_data = retrieve_access_logs(
            feature_mlflow_experiment_id=Configurations.feature_mlflow_experiment_id,
            feature_mlflow_run_id=Configurations.feature_mlflow_run_id,
            db_client=db_client,
            cache=cache,
        )
        if cfg.jobs.data.split_by_qid:
            dataset = split_by_qid(
                raw_data=raw_data,
                test_size=0.3,
            )
        else:
            dataset = random_split(
                raw_data=raw_data,
                test_size=0.3,
            )

        _model = MODELS.get_model(name=cfg.jobs.model.name)
        model = _model.model(
            early_stopping_rounds=cfg.jobs.model.params.get("early_stopping_rounds", 5),
            eval_metrics=cfg.jobs.model.params.get("eval_metrics", "mse"),
            verbose_eval=cfg.jobs.model.params.get("verbose_eval", 1),
        )
        if "params" in cfg.jobs.model.keys():
            model.reset_model(params=cfg.jobs.model.params)

        model_save_file_path = os.path.join(cwd, f"{model.name}")

        preprocessed_data, preprocess_artifact = Preprocess().run(
            likes_scaler=NumericalMinMaxScaler(),
            query_phrase_encoder=CategoricalVectorizer(),
            query_animal_category_id_encoder=CategoricalVectorizer(),
            query_animal_subcategory_id_encoder=CategoricalVectorizer(),
            likes_scaler_save_file_path=os.path.join(cwd, f"likes_scaler"),
            query_phrase_encoder_save_file_path=os.path.join(cwd, f"query_phrase_encoder"),
            query_animal_category_id_encoder_save_file_path=os.path.join(cwd, f"query_animal_category_id_encoder"),
            query_animal_subcategory_id_encoder_save_file_path=os.path.join(
                cwd, f"query_animal_subcategory_id_encoder"
            ),
            x_train=dataset.x_train,
            y_train=dataset.y_train,
            x_test=dataset.x_test,
            y_test=dataset.y_test,
            q_train=dataset.q_train,
            q_test=dataset.q_test,
        )
        mlflow.log_artifact(
            preprocess_artifact.likes_scaler_save_file_path,
            "likes_scaler",
        )
        mlflow.log_artifact(
            preprocess_artifact.query_phrase_encoder_save_file_path,
            "query_phrase_encoder",
        )
        mlflow.log_artifact(
            preprocess_artifact.query_animal_category_id_encoder_save_file_path,
            "query_animal_category_id_encoder",
        )
        mlflow.log_artifact(
            preprocess_artifact.query_animal_subcategory_id_encoder_save_file_path,
            "query_animal_subcategory_id_encoder",
        )
        preprocessed_data_file = os.path.join(cwd, f"preprocessed_data.pickle")
        with open(preprocessed_data_file, "wb") as f:
            pickle.dump(preprocessed_data, f)
        mlflow.log_artifact(
            preprocessed_data_file,
            f"preprocessed_data_file",
        )

        artifact = Trainer().train(
            model=model,
            model_save_file_path=model_save_file_path,
            x_train=preprocessed_data.x_train,
            y_train=preprocessed_data.y_train,
            x_test=preprocessed_data.x_test,
            y_test=preprocessed_data.y_test,
            q_train=preprocessed_data.q_train,
            q_test=preprocessed_data.q_test,
        )

        mlflow.log_artifact(artifact.model_file_path, "model")
        if cfg.jobs.model.get("save_onnx", False):
            mlflow.log_artifact(artifact.onnx_file_path, "onnx")

        mlflow.log_artifact(os.path.join(cwd, ".hydra/config.yaml"), "hydra_config.yaml")
        mlflow.log_artifact(os.path.join(cwd, ".hydra/hydra.yaml"), "hydra_hydra.yaml")
        mlflow.log_artifact(os.path.join(cwd, ".hydra/overrides.yaml"), "hydra_overrides.yaml")
        mlflow.log_artifact(os.path.join(cwd, "main.log"))

        mlflow.log_param("model", model.name)
        mlflow.log_params(model.params)

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
