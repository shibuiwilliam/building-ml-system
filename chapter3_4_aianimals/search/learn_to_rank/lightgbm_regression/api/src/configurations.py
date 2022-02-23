import os


class Configurations(object):
    api_title = os.getenv("API_TITLE", "learn_to_rank_lightgbm_regression")
    api_description = os.getenv("API_DESCRIPTION", "")
    version = os.getenv("VERSION", "0.0.0")

    model_version = os.getenv("MODEL_VERSION", "v0.0.0")
    model_name = f"learn_to_rank_lightgbm_regression_{model_version}"

    preprocess_file_path = os.getenv("PREPROCESS_FILE_PATH", "/opt/model/learn_to_rank_regression_preprocess.pkl")

    endpoint = os.environ["ENDPOINT"]
    input_name = os.getenv("INPUT_NAME", "input")
    output_name = os.getenv("OUTPUT_NAME", "variable")
    batch_size = int(os.getenv("BATCH_SIZE", 32))
    feature_size = int(os.getenv("FEATURE_SIZE", 200))
    retries = int(os.getenv("RETRIES", 3))
    timeout = int(os.getenv("TIMEOUT", 2))
