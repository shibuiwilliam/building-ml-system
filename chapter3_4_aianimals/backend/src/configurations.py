import os


class Configurations:
    api_title = os.getenv("API_TITLE", "aianimal_api")
    api_description = os.getenv("API_DESCRIPTION", "")
    version = os.getenv("VERSION", "0.0.0")

    run_environment = os.getenv("RUN_ENVIRONMENT", "local")
    gcs_bucket = os.getenv("GCS_BUCKET", "aianimals")

    work_directory = os.getenv("WORK_DIRECTORY", "/tmp")

    data_directory = os.environ["DATA_DIRECTORY"]
    animal_category_file = os.path.join(data_directory, "animal_category.json")
    animal_subcategory_file = os.path.join(data_directory, "animal_subcategory.json")
    animal_file = os.path.join(data_directory, "animal.json")
    user_file = os.path.join(data_directory, "user.json")

    initialize = bool(int(os.getenv("INITIALIZE", 0)))
