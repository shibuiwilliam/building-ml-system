import json
import os


class Configurations(object):
    api_title = os.getenv("API_TITLE", "learn_to_rank_lightgbm_ranker")
    api_description = os.getenv("API_DESCRIPTION", "")
    version = os.getenv("VERSION", "0.0.0")

    model_name = os.getenv("MODEL_VERSION", "learn_to_rank_lightgbm_ranker_0.0.0")

    mlflow_param_json = os.getenv("MLFLOW_PARAM_JSON", None)
    mlflow_param = {}
    if mlflow_param_json is not None:
        mlflow_param = json.loads(mlflow_param_json)
    _mlflow_experiment_id = mlflow_param.get("mlflow_experiment_id", -1)
    _mlflow_run_id = mlflow_param.get("mlflow_run_id")
    mlflow_experiment_id = int(os.getenv("MLFLOW_EXPERIMENT_ID", _mlflow_experiment_id))
    mlflow_run_id = os.getenv("MLFLOW_RUN_ID", _mlflow_run_id)

    feature_mlflow_param_json = os.getenv("FEATURE_MLFLOW_PARAM_JSON", None)
    feature_mlflow_param = {}
    if feature_mlflow_param_json is not None:
        feature_mlflow_param = json.loads(feature_mlflow_param_json)
    _feature_mlflow_experiment_id = feature_mlflow_param.get("mlflow_experiment_id", -1)
    _feature_mlflow_run_id = feature_mlflow_param.get("mlflow_run_id")
    feature_mlflow_experiment_id = int(os.getenv("FEATURE_MLFLOW_EXPERIMENT_ID", _feature_mlflow_experiment_id))
    feature_mlflow_run_id = str(os.getenv("FEATURE_MLFLOW_RUN_ID", _feature_mlflow_run_id))

    is_onnx_predictor = bool(int(os.getenv("IS_ONNX_PREDICTOR", "0")))
    predictor_batch_size = int(os.getenv("PREDICTOR_BATCH_SIZE", 32))
    predictor_input_name = os.getenv("PREDICTOR_INPUT_NAME", "inputs")
    predictor_output_name = os.getenv("PREDICTOR_OUTPUT_NAME", "outputs")

    empty_run = bool(int(os.getenv("EMPTY_RUN", "0")))
