import json
import os


class Configurations:
    run_environment = os.getenv("RUN_ENVIRONMENT", "local")

    job = os.environ["JOB"]

    save_directory = os.getenv("SAVE_DIRECTORY", "/opt/outputs")
    animal_category_vectorizer_file = os.getenv(
        "ANIMAL_CATEGORY_VECTORIZER",
        os.path.join(save_directory, "animal_category_vectorizer.pkl"),
    )
    animal_subcategory_vectorizer_file = os.getenv(
        "ANIMAL_SUBCATEGORY_VECTORIZER",
        os.path.join(save_directory, "animal_subcategory_vectorizer.pkl"),
    )
    description_vectorizer_file = os.getenv(
        "DESCRIPTION_VECTORIZER",
        os.path.join(save_directory, "description_vectorizer.pkl"),
    )
    name_vectorizer_file = os.getenv(
        "NAME_VECTORIZER",
        os.path.join(save_directory, "name_vectorizer.pkl"),
    )

    mlflow_experiment_name = os.getenv("MLFLOW_EXPERIMENT_NAME", "animal_feature_extraction")

    registry_mlflow_param_json = os.getenv("REGISTRY_MLFLOW_PARAM_JSON", None)
    registry_mlflow_param = {}
    if registry_mlflow_param_json is not None:
        registry_mlflow_param = json.loads(registry_mlflow_param_json)
    _registry_mlflow_experiment_id = registry_mlflow_param.get("mlflow_experiment_id", -1)
    _registry_mlflow_run_id = registry_mlflow_param.get("mlflow_run_id")
    registry_mlflow_experiment_id = int(os.getenv("REGISTRY_MLFLOW_EXPERIMENT_ID", _registry_mlflow_experiment_id))
    registry_mlflow_run_id = os.getenv("REGISTRY_MLFLOW_RUN_ID", _registry_mlflow_run_id)

    animal_feature_registry_queue = os.getenv("ANIMAL_FEATURE_REGISTRY_QUEUE", "animal_feature")

    empty_run = bool(int(os.getenv("EMPTY_RUN", "0")))

    feature_cache_ttl = int(os.getenv("FEATURE_CACHE_TTL", 60 * 60 * 24 * 7))
