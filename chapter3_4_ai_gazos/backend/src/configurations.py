import os


class Configurations:
    api_title = os.getenv("API_TITLE", "ai_gazos_api")
    api_description = os.getenv("API_DESCRIPTION", "")
    version = os.getenv("VERSION", "0.0.0")

    run_environment = os.getenv("RUN_ENVIRONMENT", "local")
    gcs_bucket = os.getenv("GCS_BUCKET", "ai_gazoss")

    work_directory = os.getenv("WORK_DIRECTORY", "/tmp")

    data_directory = os.environ["DATA_DIRECTORY"]
    content_file = os.path.join(data_directory, "content.json")
    user_file = os.path.join(data_directory, "user.json")

    initialize = bool(int(os.getenv("INITIALIZE", 0)))
