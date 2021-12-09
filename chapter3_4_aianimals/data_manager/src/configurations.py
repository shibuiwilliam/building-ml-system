import os


class Configurations:
    run_environment = os.getenv("RUN_ENVIRONMENT", "local")

    data_directory = os.environ["DATA_DIRECTORY"]
    animal_category_file = os.path.join(data_directory, "animal_category.json")
    animal_subcategory_file = os.path.join(data_directory, "animal_subcategory.json")
    user_file = os.path.join(data_directory, "user.json")
    animal_file = os.path.join(data_directory, "animal.json")
