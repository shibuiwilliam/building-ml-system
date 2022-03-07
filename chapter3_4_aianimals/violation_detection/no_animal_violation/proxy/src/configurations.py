import os


class Configurations:
    run_environment = os.getenv("RUN_ENVIRONMENT", "local")

    consuming_queue = os.getenv("CONSUMING_QUEUE", "no_animal_violation")
    registration_queue = os.getenv("REGISTRATION_QUEUE", "violation")

    pseudo_prediction = bool(int(os.getenv("PSEUDO_PREDICTION", "0")))
