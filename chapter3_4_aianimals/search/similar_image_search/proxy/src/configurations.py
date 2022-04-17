import json
import os


class Configurations(object):
    api_title = os.getenv("API_TITLE", "similar_image_search")
    api_description = os.getenv("API_DESCRIPTION", "")
    version = os.getenv("VERSION", "0.0.0")

    predictor_url = os.getenv("PREDICTOR_URL", "http://localhost:8501/v1/models/similar_image_search:predict")
    predictor_height = int(os.getenv("PREDICTOR_HEIGHT", "224"))
    predictor_width = int(os.getenv("PREDICTOR_WIDTH", "224"))

    threshold = int(os.getenv("THRESHOLD", 100))

    pseudo_prediction = bool(int(os.getenv("PSEUDO_PREDICTION", "0")))

    mlflow_param_json = os.getenv("MLFLOW_PARAM_JSON", None)
    if mlflow_param_json is not None:
        mlflow_param = json.loads(mlflow_param_json)
        model_name = mlflow_param.get("mlflow_run_id", None)
    else:
        model_name = None
