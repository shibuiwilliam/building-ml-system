import os


class Configurations:
    run_environment = os.getenv("RUN_ENVIRONMENT", "local")

    data_directory = os.environ["DATA_DIRECTORY"]
    animal_category_file = os.path.join(data_directory, "animal_category.json")
    animal_subcategory_file = os.path.join(data_directory, "animal_subcategory.json")
    user_file = os.path.join(data_directory, "user.json")
    animal_file = os.path.join(data_directory, "animal.json")
    violation_type_file = os.path.join(data_directory, "violation_type.json")
    violation_file = os.path.join(data_directory, "violation.json")
    access_log_file = os.path.join(data_directory, "access_logs.json")

    animal_registry_queue = os.getenv("ANIMAL_REGISTRY_QUEUE", "animal")

    animal_violation_queues = []
    for k, v in os.environ.items():
        if k.startswith("ANIMAL_VIOLATION_QUEUE_"):
            animal_violation_queues.append(v)
