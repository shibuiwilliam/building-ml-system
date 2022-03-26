import os


class Configurations:
    api_title = os.getenv("API_TITLE", "aianimal_api")
    api_description = os.getenv("API_DESCRIPTION", "")
    version = os.getenv("VERSION", "0.0.0")

    run_environment = os.getenv("RUN_ENVIRONMENT", "local")
    gcs_bucket = os.getenv("GCS_BUCKET", "aianimals")

    key_file_path = os.environ["KEY_FILE_PATH"]

    work_directory = os.getenv("WORK_DIRECTORY", "/tmp")

    animal_registry_queue = os.getenv("ANIMAL_REGISTRY_QUEUE", "animal")

    animal_violation_queues = []
    for k, v in os.environ.items():
        if k.startswith("ANIMAL_VIOLATION_QUEUE_"):
            animal_violation_queues.append(v)

    learn_to_rank_url = os.getenv("LEARN_TO_RANK_URL", None)
