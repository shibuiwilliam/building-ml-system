import json
import os


class Configurations:
    run_environment = os.getenv("RUN_ENVIRONMENT", "local")

    consuming_queue = os.getenv("CONSUMING_QUEUE", "no_animal_violation")
    registration_queue = os.getenv("REGISTRATION_QUEUE", "violation")

    off = bool(int(os.getenv("OFF", "0")))
    pseudo_prediction = bool(int(os.getenv("PSEUDO_PREDICTION", "0")))

    predictor_url = os.getenv("PREDICTOR_URL", "http://localhost:8501/v1/models/no_animal_violation:predict")
    predictor_height = int(os.getenv("PREDICTOR_HEIGHT", "224"))
    predictor_width = int(os.getenv("PREDICTOR_WIDTH", "224"))

    mlflow_param_json = os.getenv("MLFLOW_PARAM_JSON", None)
    if mlflow_param_json is not None:
        mlflow_param = json.loads(mlflow_param_json)
        model_name = mlflow_param.get("mlflow_run_id", "administrator")
    else:
        model_name = "administrator"

    logging_file = "/opt/src/logging.ini"
