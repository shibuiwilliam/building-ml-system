import json
import os


class Configurations(object):
    mlflow_param_json = os.getenv("MLFLOW_PARAM_JSON", None)
    mlflow_param = {}
    if mlflow_param_json is not None:
        mlflow_param = json.loads(mlflow_param_json)
    _mlflow_experiment_id = mlflow_param.get("mlflow_experiment_id", -1)
    _mlflow_run_id = mlflow_param.get("mlflow_run_id")
    mlflow_experiment_id = int(os.getenv("MLFLOW_EXPERIMENT_ID", _mlflow_experiment_id))
    mlflow_run_id = os.getenv("MLFLOW_RUN_ID", _mlflow_run_id)

    _target_artifacts = os.getenv("TARGET_ARTIFACTS", "saved_model")
    target_artifacts = _target_artifacts.split(",")

    _target_urls = os.getenv("TARGET_URLS", "")
    target_urls = _target_urls.split(",")

    target_directory = os.getenv("TARGET_DIRECTORY", "/tmp/")
