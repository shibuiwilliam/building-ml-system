import os


class DatabaseConfigurations(object):
    postgresql_user = os.getenv("POSTGRESQL_USER")
    postgresql_password = os.getenv("POSTGRESQL_PASSWORD")
    postgresql_port = int(os.getenv("POSTGRESQL_PORT", 5432))
    postgresql_dbname = os.getenv("POSTGRESQL_DBNAME")
    postgresql_host = os.getenv("POSTGRESQL_HOST")
    connection_string = f"host={postgresql_host} port={postgresql_port} dbname={postgresql_dbname} user={postgresql_user} password={postgresql_password}"


class Configurations(object):
    wait_second = int(os.getenv("WAIT_SECOND", 60))
