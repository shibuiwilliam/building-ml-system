from logger import configure_logger
from service import ItemSalesPredictionEvaluationService, ItemSalesService, ItemService, StoreService
from view import build

logger = configure_logger(__name__)


def main():
    logger.info("now loading...")
    logger.info("start fun time")
    store_service = StoreService()
    item_service = ItemService()
    item_sales_service = ItemSalesService()
    item_sales_prediction_evaluation_service = ItemSalesPredictionEvaluationService()
    build(
        store_service=store_service,
        item_service=item_service,
        item_sales_service=item_sales_service,
        item_sales_prediction_evaluation_service=item_sales_prediction_evaluation_service,
    )


if __name__ == "__main__":
    main()
