import os


class DatabaseConfigurations(object):
    postgresql_user = os.getenv("POSTGRESQL_USER")
    postgresql_password = os.getenv("POSTGRESQL_PASSWORD")
    postgresql_port = int(os.getenv("POSTGRESQL_PORT", 5432))
    postgresql_dbname = os.getenv("POSTGRESQL_DBNAME")
    postgresql_host = os.getenv("POSTGRESQL_HOST")
    connection_string = f"host={postgresql_host} port={postgresql_port} dbname={postgresql_dbname} user={postgresql_user} password={postgresql_password}"


class Configurations(object):
    api_title = os.getenv("API_TITLE", "demand_forecasting")
    api_description = os.getenv("API_DESCRIPTION", "demand forecasting data api")
    api_version = os.getenv("API_VERSION", "0")

    data_directory = os.getenv("DATA_DIRECTORY", "/opt/data/")
    create_sql_file_path = os.path.join(data_directory, os.getenv("CREATE_SQL", "create.sql"))
    region_file_path = os.path.join(data_directory, os.getenv("REGION_FILE", "regions.csv"))
    store_file_path = os.path.join(data_directory, os.getenv("STORE_FILE", "stores.csv"))
    item_file_path = os.path.join(data_directory, os.getenv("ITEM_FILE", "items.csv"))
    item_price_path = os.path.join(data_directory, os.getenv("ITEM_PRICE", "item_prices.csv"))
    item_sale_records_2017_2019_path = os.path.join(
        data_directory, os.getenv("ITEM_SALE_RECORDS_FILE", "item_sale_records_2017_2019.csv")
    )

    initialize_tables = bool(os.getenv("INITIALIZE_TABLES", 1))
    initialize_data = bool(os.getenv("INITIALIZE_DATA", 1))
