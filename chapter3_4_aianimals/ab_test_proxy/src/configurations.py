import os


class Configurations:
    api_title = os.getenv("API_TITLE", "aianimal_ab_test_proxy")
    api_description = os.getenv("API_DESCRIPTION", "")
    version = os.getenv("VERSION", "0.0.0")

    run_environment = os.getenv("RUN_ENVIRONMENT", "local")

    ab_test_configuration = os.environ["AB_TEST_CONFIGURATION"]
