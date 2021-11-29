import os


class Configurations:
    api_title = os.getenv("API_TITLE", "aianimal_api")
    api_description = os.getenv("API_DESCRIPTION", "")
    version = os.getenv("VERSION", "0.0.0")
