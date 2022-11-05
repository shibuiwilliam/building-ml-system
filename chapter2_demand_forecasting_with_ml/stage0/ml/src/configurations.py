import os


class Configurations(object):
    target_config_name = os.getenv("TARGET_CONFIG_NAME", "2020_52")
