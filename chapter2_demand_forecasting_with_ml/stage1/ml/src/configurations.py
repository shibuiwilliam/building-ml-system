import os


class Configurations(object):
    target_config_name = os.getenv("TARGET_CONFIG_NAME", "default")

    target_item = os.getenv("TARGET_ITEM", "ALL")
    target_store = os.getenv("TARGET_STORE", "ALL")
    target_region = os.getenv("TARGET_REGION", "ALL")

    _target_items = os.getenv("TARGET_ITEMS", "ALL")
    target_items = _target_items.split(",") if _target_items != "ALL" else [_target_items]
    _target_stores = os.getenv("TARGET_STORES", "ALL")
    target_stores = _target_stores.split(",") if _target_stores != "ALL" else [_target_stores]

    target_year = os.getenv("TARGET_YEAR", None)
    if target_year is not None:
        target_year = int(target_year)
    target_week = os.getenv("TARGET_WEEK", None)
    if target_week is not None:
        target_week = int(target_week)
