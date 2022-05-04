import json
import os


class Configurations:
    run_environment = os.getenv("RUN_ENVIRONMENT", "local")

    job = os.environ["JOB"]
    model_path = os.environ["MODEL_PATH"]

    search_top_n = int(os.getenv("SEARCH_TOP_N", 100))
    similar_top_n = int(os.getenv("SIMILAR_TOP_N", 10))

    logging_file = "/opt/src/logging.ini"
