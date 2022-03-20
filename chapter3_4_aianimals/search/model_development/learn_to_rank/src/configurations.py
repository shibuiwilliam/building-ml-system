import json
import os


class Configurations:
    feature_mlflow_param_json = os.getenv("FEATURE_MLFLOW_PARAM_JSON", None)
    feature_mlflow_param = {}
    if feature_mlflow_param_json is not None:
        with open(feature_mlflow_param_json, "r") as f:
            feature_mlflow_param = json.load(f)
    _feature_mlflow_experiment_id = feature_mlflow_param.get("mlflow_experiment_id")
    _feature_mlflow_run_id = feature_mlflow_param.get("mlflow_run_id")

    feature_mlflow_experiment_id = int(os.getenv("FEATURE_MLFLOW_EXPERIMENT_ID", _feature_mlflow_experiment_id))
    feature_mlflow_run_id = str(os.getenv("FEATURE_MLFLOW_RUN_ID", _feature_mlflow_run_id))

    if feature_mlflow_experiment_id is None or feature_mlflow_run_id is None:
        raise ValueError("feature_mlflow_experiment_id and feature_mlflow_run_id cannot be None")
