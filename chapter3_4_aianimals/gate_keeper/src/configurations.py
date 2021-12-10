import os


class Configurations:
    run_environment = os.getenv("RUN_ENVIRONMENT", "local")
