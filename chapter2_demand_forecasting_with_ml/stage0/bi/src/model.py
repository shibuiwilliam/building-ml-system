from datetime import date
from typing import Dict, List, Optional

import pandas as pd
from logger import configure_logger
from schema import BASE_SCHEMA, WEEKLY_PREDICTION_SCHEMA, Item, Store

logger = configure_logger(__name__)


class Container(object):
    def __init__(self):
        self.sales_df: pd.DataFrame = None
        self.prediction_df: pd.DataFrame = None
        self.prediction_record_df: pd.DataFrame = None

    def load_df(
        self,
        file_path: str,
    ) -> pd.DataFrame:
        logger.info(f"read {file_path}")
        df = pd.read_csv(file_path)
        logger.info(
            f"""
read {file_path}
shape: {df.shape}
columns: {df.columns}
        """
        )
        return df

    def load_sales_df(
        self,
        file_path: str,
    ):
        self.sales_df = self.load_df(file_path=file_path)
        self.sales_df["date"] = pd.to_datetime(self.sales_df["date"])
        self.sales_df["year"] = self.sales_df.date.dt.year
        self.sales_df = BASE_SCHEMA.validate(self.sales_df)
        logger.info(
            f"""
formatted {file_path}
shape: {self.sales_df.shape}
columns: {self.sales_df.columns}
        """
        )

    def load_prediction_df(
        self,
        prediction_file_path: str,
        prediction_record_file_path: str,
    ):
        self.prediction_df = self.load_df(file_path=prediction_file_path)
        self.prediction_df = WEEKLY_PREDICTION_SCHEMA.validate(self.prediction_df)
        logger.info(
            f"""
formatted {prediction_file_path}
shape: {self.prediction_df.shape}
columns: {self.prediction_df.columns}
        """
        )

        self.prediction_record_df = self.load_df(file_path=prediction_record_file_path)
        self.prediction_record_df["date"] = pd.to_datetime(self.prediction_record_df.date)
        self.prediction_record_df["year"] = self.prediction_record_df.date.dt.year
        self.prediction_record_df = BASE_SCHEMA.validate(self.prediction_record_df)
        logger.info(
            f"""
formatted {prediction_record_file_path}
shape: {self.prediction_record_df.shape}
columns: {self.prediction_record_df.columns}
        """
        )


class StoreRepository(object):
    def __init__(self):
        pass

    def select(
        self,
        container: Container,
    ) -> List[Store]:
        stores = container.sales_df.store.unique()
        data = [Store(name=s) for s in stores]
        return data


class ItemRepository(object):
    def __init__(self):
        pass

    def select(
        self,
        container: Container,
    ) -> List[Item]:
        items = container.sales_df.item.unique()
        data = [Item(name=i) for i in items]
        return data


class ItemSalesRepository(object):
    def __init__(self):
        pass

    def select(
        self,
        container: Container,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        year: Optional[int] = None,
        day_of_week: Optional[str] = None,
        item: Optional[str] = None,
        store: Optional[str] = None,
    ) -> pd.DataFrame:
        df = container.sales_df
        if date_from is not None:
            df = df[df.date >= date_from]
        if date_to is not None:
            df = df[df.date <= date_to]
        if year is not None:
            df = df[df.year == year]
        if day_of_week is not None:
            df = df[df.day_of_week == day_of_week]
        if item is not None:
            df = df[df.item == item]
        if store is not None:
            df = df[df.store == store]
        return df


class ItemWeeklySalesPredictionsRepository(object):
    def __init__(self):
        pass

    def select(
        self,
        container: Container,
        item: Optional[str] = None,
        store: Optional[str] = None,
    ) -> pd.DataFrame:
        df = container.prediction_df
        if item is not None:
            df = df[df.item == item]
        if store is not None:
            df = df[df.store == store]
        return df
