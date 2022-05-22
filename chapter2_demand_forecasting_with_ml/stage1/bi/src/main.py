from db_client import PostgreSQLClient
from logger import configure_logger
from service import ItemSalesPredictionEvaluationService, ItemSalesService, ItemService, RegionService, StoreService
from view import build

logger = configure_logger(__name__)


def main():
    logger.info("now loading...")
    logger.info("start fun time")
    db_client = PostgreSQLClient()
    region_service = RegionService(db_client=db_client)
    store_service = StoreService(db_client=db_client)
    item_service = ItemService(db_client=db_client)
    item_sales_service = ItemSalesService(db_client=db_client)
    item_sales_prediction_evaluation_service = ItemSalesPredictionEvaluationService(db_client=db_client)
    build(
        region_service=region_service,
        store_service=store_service,
        item_service=item_service,
        item_sales_service=item_sales_service,
        item_sales_prediction_evaluation_service=item_sales_prediction_evaluation_service,
    )


if __name__ == "__main__":
    main()
