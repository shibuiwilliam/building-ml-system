import os
from typing import Dict

from constants import CONSTANT, TASK_TYPE


class Configurations(object):
    __postgres_username = os.getenv("POSTGRES_USER")
    __postgres_password = os.getenv("POSTGRES_PASSWORD")
    __postgres_port = int(os.getenv("POSTGRES_PORT", 5432))
    __postgres_db = os.getenv("POSTGRES_DB")
    __postgres_server = os.getenv("POSTGRES_SERVER")
    sql_alchemy_database_url = f"postgresql://{__postgres_username}:{__postgres_password}@{__postgres_server}:{__postgres_port}/{__postgres_db}?client_encoding=utf8"
