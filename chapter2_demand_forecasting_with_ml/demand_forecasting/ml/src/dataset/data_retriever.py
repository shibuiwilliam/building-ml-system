from abc import ABC, abstractmethod
from datetime import date, datetime, time
from typing import List, Optional

import pandas as pd
from data_client.data_client import ItemClient
from pandera import DataFrameSchema
from src.dataset.schema import BASE_SCHEMA, PREDICTION_SCHEMA, ItemPrice, ItemSale, PredictionTarget
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


def save_df_to_csv(
    df: pd.DataFrame,
    file_path: str,
):
    logger.info(f"save dataframe to {file_path}")
    df.to_csv(file_path, index=False)


def load_df_from_csv(
    file_path: str,
) -> pd.DataFrame:
    logger.info(f"load dataframe from {file_path}")
    return pd.read_csv(file_path)


class BaseDataRetriever(ABC):
    def __init__(
        self,
        api_endpoint: str,
        timeout: int = 10,
        retries: int = 3,
    ):
        self.api_endpoint = api_endpoint
        self.timeout = timeout
        self.retries = retries

    @abstractmethod
    def ping(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def retrieve_item_sale(
        self,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        store_name: Optional[str] = None,
        store_id: Optional[str] = None,
        item_price_id: Optional[str] = None,
        quantity: Optional[int] = None,
        sold_at: Optional[date] = None,
        day_of_week: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ItemSale]:
        raise NotImplementedError

    @abstractmethod
    def retrieve_item_price(
        self,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        applied_from: Optional[date] = None,
        applied_to: Optional[date] = None,
        applied_at: Optional[date] = None,
    ) -> List[ItemPrice]:
        raise NotImplementedError


class DataRetriever(BaseDataRetriever):
    def __init__(
        self,
        api_endpoint: str,
        timeout: int = 10,
        retries: int = 3,
    ):
        super().__init__(
            api_endpoint=api_endpoint,
            timeout=timeout,
            retries=retries,
        )
        self.item_client = ItemClient(
            timeout=self.timeout,
            retries=self.retries,
            api_endpoint=self.api_endpoint,
        )

    def ping(self) -> bool:
        logger.info("send ping...")
        response = self.item_client.ping()
        return response

    def retrieve_item_sale(
        self,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        store_name: Optional[str] = None,
        store_id: Optional[str] = None,
        item_price_id: Optional[str] = None,
        quantity: Optional[int] = None,
        sold_at: Optional[date] = None,
        day_of_week: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ItemSale]:
        response = self.item_client.retrieve_item_sale(
            id=id,
            item_name=item_name,
            item_id=item_id,
            store_name=store_name,
            store_id=store_id,
            item_price_id=item_price_id,
            quantity=quantity,
            sold_at=sold_at,
            day_of_week=day_of_week,
            limit=limit,
            offset=offset,
        )
        item_sales = [ItemSale(**r.dict()) for r in response]
        return item_sales

    def retrieve_item_price(
        self,
        id: Optional[str] = None,
        item_name: Optional[str] = None,
        item_id: Optional[str] = None,
        applied_from: Optional[date] = None,
        applied_to: Optional[date] = None,
        applied_at: Optional[date] = None,
    ) -> List[ItemPrice]:
        response = self.item_client.retrieve_item_price(
            id=id,
            item_name=item_name,
            item_id=item_id,
            applied_from=applied_from,
            applied_to=applied_to,
            applied_at=applied_at,
        )
        item_sales = [ItemPrice(**r.dict()) for r in response]
        return item_sales

    def train_data_to_dataframe(
        self,
        item_sales: List[ItemSale],
        schema: DataFrameSchema = BASE_SCHEMA,
    ) -> pd.DataFrame:
        data = []
        for item_sale in item_sales:
            data.append(
                {
                    "date": datetime.combine(item_sale.sold_at, time()),
                    "day_of_week": item_sale.day_of_week,
                    "store": item_sale.store_name,
                    "item": item_sale.item_name,
                    "item_price": item_sale.price,
                    "sales": item_sale.quantity,
                    "total_sales": item_sale.total_sales,
                }
            )
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df = schema.validate(df)
        logger.info("done load data")
        return df

    def prediction_data_to_dataframe(
        self,
        prediction_targets: List[PredictionTarget],
        schema: DataFrameSchema = PREDICTION_SCHEMA,
    ) -> pd.DataFrame:
        data = []
        for prediction_target in prediction_targets:
            data.append(
                {
                    "date": datetime.combine(prediction_target.date, time()),
                    "day_of_week": prediction_target.day_of_week,
                    "store": prediction_target.store_name,
                    "item": prediction_target.item_name,
                    "item_price": prediction_target.price,
                }
            )
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df = schema.validate(df)
        logger.info("done load data")
        return df
