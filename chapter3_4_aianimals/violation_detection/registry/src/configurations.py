import os


class Configurations:
    run_environment = os.getenv("RUN_ENVIRONMENT", "local")

    violation_queue = os.getenv("VIOLATION_QUEUE", "violation")

    logging_file = "/opt/src/logging.ini"
