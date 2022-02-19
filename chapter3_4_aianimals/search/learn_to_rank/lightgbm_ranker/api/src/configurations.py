import os


class Configurations(object):
    api_title = os.getenv("API_TITLE", "learn_to_rank_lightgbm_ranker")
    api_description = os.getenv("API_DESCRIPTION", "")
    version = os.getenv("VERSION", "0.0.0")

    model_version = os.getenv("MODEL_VERSION", "v0.0.0")
    model_name = f"learn_to_rank_lightgbm_ranker_{model_version}"

    preprocess_file_path = os.environ["PREPROCESS_FILE_PATH"]
    predictor_file_path = os.environ["PREDICTOR_FILE_PATH"]
