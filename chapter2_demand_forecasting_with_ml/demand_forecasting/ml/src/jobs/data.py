import dataclasses
import os
from datetime import date, datetime, timedelta
from typing import List, Optional

import pandas as pd
from pandera import DataFrameSchema
from src.dataset.data_retriever import BaseDataRetriever, save_df_to_csv
from src.dataset.schema import BASE_SCHEMA, DAYS_OF_WEEK, ITEMS, STORES, PredictionTarget
from src.utils.logger import configure_logger

logger = configure_logger(__name__)


@dataclasses.dataclass(frozen=True)
class DataFilePath(object):
    train_file_path: str
    prediction_file_path: str


class DataJob(object):
    def __init__(
        self,
        data_retriever: BaseDataRetriever,
        stores: Optional[List[str]] = None,
        items: Optional[List[str]] = None,
        save_file_directory: str = "/tmp",
        base_schema: DataFrameSchema = BASE_SCHEMA,
    ):
        self.data_retriever = data_retriever
        self.stores = stores
        self.items = items
        self.base_schema = base_schema
        self.save_file_directory = save_file_directory

        self.limit = 1000

    def __get_now(self) -> str:
        return datetime.today().strftime("%Y%m%d_%H%M%S")

    def __make_directory(
        self,
        job_name: str,
        train_start_date: Optional[date] = None,
        train_end_date: Optional[date] = None,
        test_start_date: Optional[date] = None,
        test_end_date: Optional[date] = None,
        predict_start_date: Optional[date] = None,
        predict_end_date: Optional[date] = None,
    ) -> str:
        logger.info(
            f"make directory for {train_start_date} to {train_end_date}; {test_start_date} to {test_end_date}; {predict_start_date} to {predict_end_date}"
        )
        subdirectory = f"{job_name}"

        if train_start_date is not None:
            _train_start_date = train_start_date.strftime("%Y%m%d")
            subdirectory += f"_{_train_start_date}"
        if train_end_date is not None:
            _train_end_date = train_end_date.strftime("%Y%m%d")
            subdirectory += f"_{_train_end_date}"

        if test_start_date is not None:
            _test_start_date = test_start_date.strftime("%Y%m%d")
            subdirectory += f"_{_test_start_date}"
        if test_end_date is not None:
            _test_end_date = test_end_date.strftime("%Y%m%d")
            subdirectory += f"_{_test_end_date}"

        if predict_start_date is not None:
            _predict_start_date = predict_start_date.strftime("%Y%m%d")
            subdirectory += f"_{_predict_start_date}"
        if predict_end_date is not None:
            _predict_end_date = predict_end_date.strftime("%Y%m%d")
            subdirectory += f"_{_predict_end_date}"

        directory = os.path.join(self.save_file_directory, subdirectory)
        os.makedirs(directory, exist_ok=True)

        logger.info(f"made directory: {directory}")
        return directory

    def __list_dates_between_two_dates(
        self,
        start_date: date,
        end_date: date,
    ) -> List[date]:
        if start_date == end_date:
            return [start_date]
        dates = []
        for x in range((end_date - start_date).days):
            dates.append(start_date + timedelta(days=x))
        dates.append(end_date)
        return dates

    def retrieve(
        self,
        train_start_date: Optional[date] = None,
        train_end_date: Optional[date] = None,
        test_start_date: Optional[date] = None,
        test_end_date: Optional[date] = None,
        predict_start_date: Optional[date] = None,
        predict_end_date: Optional[date] = None,
    ) -> DataFilePath:
        logger.info("start data retrieval...")

        directory = self.__make_directory(
            job_name="data_retrieval",
            train_start_date=train_start_date,
            train_end_date=train_end_date,
            test_start_date=test_start_date,
            test_end_date=test_end_date,
            predict_start_date=predict_start_date,
            predict_end_date=predict_end_date,
        )

        train_data_record = []
        train_file_path = os.path.join(directory, f"train_{self.__get_now()}.csv")
        prediction_data_record = []
        prediction_file_path = os.path.join(directory, f"prediction_{self.__get_now()}.csv")

        if train_start_date is not None and train_end_date is not None:
            dates = self.__list_dates_between_two_dates(
                start_date=train_start_date,
                end_date=train_end_date,
            )
            for d in dates:
                offset = 0
                while True:
                    item_sales = self.data_retriever.retrieve_item_sale(
                        sold_at=d,
                        limit=self.limit,
                        offset=offset,
                    )
                    if len(item_sales) == 0:
                        break
                    train_data_record.extend(item_sales)
                    offset += self.limit

        if test_start_date is not None and test_end_date is not None:
            dates = self.__list_dates_between_two_dates(
                start_date=test_start_date,
                end_date=test_end_date,
            )
            for d in dates:
                offset = 0
                while True:
                    item_sales = self.data_retriever.retrieve_item_sale(
                        sold_at=d,
                        limit=self.limit,
                        offset=offset,
                    )
                    if len(item_sales) == 0:
                        break
                    train_data_record.extend(item_sales)
                    offset += self.limit

        if len(train_data_record) > 0:
            train_df = self.data_retriever.train_data_to_dataframe(item_sales=train_data_record)
            save_df_to_csv(
                df=train_df,
                file_path=train_file_path,
            )

        if predict_start_date is not None and predict_end_date is not None:
            dates = self.__list_dates_between_two_dates(
                start_date=predict_start_date,
                end_date=predict_end_date,
            )
            _stores = self.stores if self.stores is not None else STORES
            _items = self.items if self.items is not None else ITEMS
            for d in dates:
                for store in _stores:
                    for item in _items:
                        item_prices = self.data_retriever.retrieve_item_price(item_name=item)
                        item_price = 0
                        if len(item_prices) > 0:
                            item_price = item_prices[0].price
                        prediction_data_record.append(
                            PredictionTarget(
                                store_name=store,
                                item_name=item,
                                date=d,
                                day_of_week=DAYS_OF_WEEK[d.isocalendar().weekday - 1],
                                price=item_price,
                            )
                        )

        if len(prediction_data_record) > 0:
            prediction_df = self.data_retriever.prediction_data_to_dataframe(prediction_targets=prediction_data_record)
            save_df_to_csv(
                df=prediction_df,
                file_path=prediction_file_path,
            )

        logger.info("done data retrieval...")
        return DataFilePath(
            train_file_path=train_file_path,
            prediction_file_path=prediction_file_path,
        )
