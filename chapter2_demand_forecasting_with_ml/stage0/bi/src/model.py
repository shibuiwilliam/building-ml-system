from datetime import date
from typing import Dict, List, Optional

import pandas as pd
from logger import configure_logger
from schema import Item, Store, BASE_SCHEMA, WEEKLY_PREDICTION_SCHEMA

logger = configure_logger(__name__)


class Container(object):
    def __init__(self):
        self.sales_df: pd.DataFrame = None
        self.prediction_dict: Dict[int, Dict[int, pd.DataFrame]] = {}

    def load_df(
        self,
        file_path: str,
    ) -> pd.DataFrame:
        return pd.read_csv(file_path)

    def load_sales_df(
        self,
        file_path: str,
    ):
        self.sales_df = self.load_df(file_path=file_path)
        self.sales_df["date"] = pd.to_datetime(self.sales_df["date"]).dt.date
        self.sales_df["year"] = self.sales_df.date.dt.year
        self.sales_df = BASE_SCHEMA.validate(self.sales_df)

    def load_prediction_df(
        self,
        file_path: str,
        year: int,
        week_of_year: int,
    ):
        df = self.load_df(file_path=file_path)
        df = WEEKLY_PREDICTION_SCHEMA.validate(df)
        self.prediction_dict[year] = {week_of_year: df}


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
        year: int,
        week_of_year: int,
        item: Optional[str] = None,
        store: Optional[str] = None,
    ) -> pd.DataFrame:
        df = container.prediction_dict[year][week_of_year]
        if item is not None:
            df = df[df.item == item]
        if store is not None:
            df = df[df.store == store]
        return df
