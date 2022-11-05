import os


class Configurations:
    run_environment = os.getenv("RUN_ENVIRONMENT", "local")

    violation_queue = os.getenv("VIOLATION_QUEUE", "violation")

    thresholds = {}
    for k, v in os.environ.items():
        if k.startswith("THRESHOLD_"):
            thresholds[k.replace("THRESHOLD_", "")] = float(v)

    logging_file = "/opt/src/logging.ini"
