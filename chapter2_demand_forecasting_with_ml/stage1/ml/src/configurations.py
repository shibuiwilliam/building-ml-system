import os


class Configurations(object):
    target_config_name = os.getenv("TARGET_CONFIG_NAME", "default")

    target_item = os.getenv("TARGET_ITEM", "ALL")
    target_store = os.getenv("TARGET_STORE", "ALL")
    target_region = os.getenv("TARGET_REGION", "ALL")
