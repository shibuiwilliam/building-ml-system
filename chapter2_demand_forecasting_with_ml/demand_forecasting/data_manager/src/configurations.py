import os
from typing import Dict

from src.constants import CONSTANT


class DatabaseConfigurations(object):
    __postgres_username = os.getenv("POSTGRES_USER")
    __postgres_password = os.getenv("POSTGRES_PASSWORD")
    __postgres_port = int(os.getenv("POSTGRES_PORT", 5432))
    __postgres_db = os.getenv("POSTGRES_DB")
    __postgres_server = os.getenv("POSTGRES_SERVER")
    sql_alchemy_database_url = f"postgresql://{__postgres_username}:{__postgres_password}@{__postgres_server}:{__postgres_port}/{__postgres_db}?client_encoding=utf8"


class Configurations(object):
    data_directory = os.getenv("DATA_DIRECTORY", "/opt/data/")
    region_file_path = os.path.join(data_directory, os.getenv("REGION_FILE", "regions.csv"))
    store_file_path = os.path.join(data_directory, os.getenv("STORE_FILE", "stores.csv"))
    item_file_path = os.path.join(data_directory, os.getenv("ITEM_FILE", "items.csv"))
    item_price_path = os.path.join(data_directory, os.getenv("ITEM_PRICE", "item_prices.csv"))
    item_sale_records_2017_2019_path = os.path.join(
        data_directory, os.getenv("ITEM_SALE_RECORDS_FILE", "item_sale_records_2017_2019.csv")
    )
