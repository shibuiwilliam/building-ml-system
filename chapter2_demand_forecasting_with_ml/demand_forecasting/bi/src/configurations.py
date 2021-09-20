import os


class Configurations(object):
    api_endpoint = os.getenv("API_ENDPOINT", "http://data_manager:8000/v0")
    wait_second = int(os.getenv("WAIT_SECOND", 60))
