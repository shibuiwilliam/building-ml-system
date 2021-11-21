import os


class Configurations:
    item_sales_record_file: str = os.environ["ITEM_SALES_RECORD_FILE"]
    item_sales_prediction_dir: str = os.environ["ITEM_SALES_PREDICTION_DIR"]
