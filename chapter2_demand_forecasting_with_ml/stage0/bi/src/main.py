from logger import configure_logger
from view import build
from view_model import (
    ItemSalesPredictionEvaluationViewModel,
    ItemSalesViewModel,
    ItemViewModel,
    StoreViewModel,
)

logger = configure_logger(__name__)


def main():
    logger.info("now loading...")
    logger.info("start fun time")
    store_view_model = StoreViewModel()
    item_view_model = ItemViewModel()
    item_sales_view_model = ItemSalesViewModel()
    item_sales_prediction_evaluation_view_model = ItemSalesPredictionEvaluationViewModel()
    build(
        store_view_model=store_view_model,
        item_view_model=item_view_model,
        item_sales_view_model=item_sales_view_model,
        item_sales_prediction_evaluation_view_model=item_sales_prediction_evaluation_view_model,
    )


if __name__ == "__main__":
    main()
